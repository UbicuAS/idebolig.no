<?php
/**
 * Kontaktskjema for idebolig.no — IB1.11
 *
 * Tar imot innsending fra kontaktsiden og sender den videre på e-post.
 * Ligger i webroten (/www/skjema.php). Hemmeligheter ligger IKKE her, men i
 * ../skjema-config.php — altså utenfor webroten, der den aldri kan serveres ut.
 *
 * Lagdelt spamvern, i den rekkefølgen sjekkene kjører:
 *   1. Bare POST slipper inn
 *   2. Honeypot — skjult felt som bare roboter fyller ut
 *   3. Tidssperre — innsending under 3 sekunder etter sidelast er en bot
 *   4. Rate-limiting per IP
 *   5. Cloudflare Turnstile, verifisert på serversiden
 *   6. Innholdsvalidering og spamheuristikk
 *
 * Avvisninger er bevisst ordknappe utad. En bot skal ikke få vite hvilken
 * sjekk den gikk på.
 */

declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');

/** Svar og avslutt. */
function svar(int $kode, string $melding, bool $ok = false): never {
    http_response_code($kode);
    echo json_encode(['ok' => $ok, 'melding' => $melding], JSON_UNESCAPED_UNICODE);
    exit;
}

// --- Konfigurasjon utenfor webroten -----------------------------------------
// Vi går oppover i katalogtreet og tar den første skjema-config.php vi finner.
// I produksjon ligger skriptet i /www og konfigurasjonen ett hakk over. Under
// generalprøven ligger skriptet i /www/ny, altså ett hakk lenger ned — da
// finner søket den likevel, uten at noe må konfigureres om.
$configsti = null;
$mappe = __DIR__;
for ($i = 0; $i < 4; $i++) {
    $mappe = dirname($mappe);
    if ($mappe === '' || $mappe === '/' || $mappe === '.') {
        break;
    }
    if (is_readable($mappe . '/skjema-config.php')) {
        $configsti = $mappe . '/skjema-config.php';
        break;
    }
}
if ($configsti === null) {
    error_log('skjema.php: fant ingen skjema-config.php over ' . __DIR__);
    svar(500, 'Skjemaet er ikke satt opp riktig. Send oss gjerne en e-post i stedet.');
}
$cfg = require $configsti;

$mottaker      = $cfg['mottaker']          ?? '';
$avsender      = $cfg['avsender']          ?? '';
$turnstile_key = $cfg['turnstile_secret']  ?? '';
$loggmappe     = $cfg['loggmappe']         ?? (dirname(__DIR__) . '/skjema-logg');
$maks_per_time = (int)($cfg['maks_per_time'] ?? 5);

if ($mottaker === '' || $avsender === '' || $turnstile_key === '') {
    error_log('skjema.php: mangler mottaker, avsender eller turnstile_secret i config');
    svar(500, 'Skjemaet er ikke satt opp riktig. Send oss gjerne en e-post i stedet.');
}

// --- 1. Bare POST ------------------------------------------------------------
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    svar(405, 'Bruk skjemaet på kontaktsiden.');
}

$rå = file_get_contents('php://input');
$inn = json_decode((string)$rå, true);
if (!is_array($inn)) {
    $inn = $_POST;
}

/** Hent felt som trimmet streng. */
function felt(array $inn, string $navn): string {
    $v = $inn[$navn] ?? '';
    return is_string($v) ? trim($v) : '';
}

$navn    = felt($inn, 'navn');
$epost   = felt($inn, 'epost');
$telefon = felt($inn, 'telefon');
$emne    = felt($inn, 'emne');
$melding = felt($inn, 'melding');
$firma   = felt($inn, 'firma');            // honeypot
$token   = felt($inn, 'turnstile');
$ms      = (int)($inn['ms'] ?? 0);          // millisekunder siden sidelast

// --- 2. Honeypot -------------------------------------------------------------
// Feltet er skjult for mennesker. Er det fylt ut, er det en bot. Vi svarer
// «takk» så boten tror den lyktes og ikke prøver en annen vei.
if ($firma !== '') {
    svar(200, 'Takk for henvendelsen!', true);
}

// --- 3. Tidssperre -----------------------------------------------------------
if ($ms > 0 && $ms < 3000) {
    svar(200, 'Takk for henvendelsen!', true);
}

// --- 4. Rate-limiting per IP -------------------------------------------------
$ip = (string)($_SERVER['REMOTE_ADDR'] ?? 'ukjent');
if (!is_dir($loggmappe)) {
    @mkdir($loggmappe, 0700, true);
}
if (is_dir($loggmappe) && is_writable($loggmappe)) {
    $fil = $loggmappe . '/' . hash('sha256', $ip) . '.txt';
    $nå = time();
    $tidspunkter = [];
    if (is_readable($fil)) {
        $tidspunkter = array_filter(
            array_map('intval', explode(',', (string)file_get_contents($fil))),
            fn(int $t): bool => $t > $nå - 3600
        );
    }
    if (count($tidspunkter) >= $maks_per_time) {
        svar(429, 'Du har sendt flere henvendelser på kort tid. Prøv igjen om en time, eller ring oss.');
    }
    $tidspunkter[] = $nå;
    @file_put_contents($fil, implode(',', $tidspunkter), LOCK_EX);
}

// --- 5. Turnstile ------------------------------------------------------------
if ($token === '') {
    svar(400, 'Bot-sjekken ble ikke fullført. Last siden på nytt og prøv igjen.');
}

$ktx = stream_context_create([
    'http' => [
        'method'        => 'POST',
        'header'        => "Content-Type: application/x-www-form-urlencoded\r\n",
        'content'       => http_build_query([
            'secret'   => $turnstile_key,
            'response' => $token,
            'remoteip' => $ip,
        ]),
        'timeout'       => 10,
        'ignore_errors' => true,
    ],
]);
$tsvar = @file_get_contents('https://challenges.cloudflare.com/turnstile/v0/siteverify', false, $ktx);
$tdata = is_string($tsvar) ? json_decode($tsvar, true) : null;

if (!is_array($tdata) || ($tdata['success'] ?? false) !== true) {
    error_log('skjema.php: Turnstile avviste — ' . json_encode($tdata['error-codes'] ?? []));
    svar(400, 'Bot-sjekken feilet. Last siden på nytt og prøv igjen.');
}

// --- 6. Validering -----------------------------------------------------------
$feil = [];

if (mb_strlen($navn) < 2 || mb_strlen($navn) > 100) {
    $feil[] = 'navn';
}
if (!filter_var($epost, FILTER_VALIDATE_EMAIL) || mb_strlen($epost) > 190) {
    $feil[] = 'epost';
}
if (mb_strlen($melding) < 10 || mb_strlen($melding) > 5000) {
    $feil[] = 'melding';
}
if ($telefon !== '' && !preg_match('/^[\d\s+()\-]{6,25}$/', $telefon)) {
    $feil[] = 'telefon';
}
if ($feil !== []) {
    svar(422, 'Sjekk at navn, e-post og melding er fylt ut riktig.');
}

// Header-injeksjon: linjeskift i felt som havner i e-posthoder
if (preg_match('/[\r\n]/', $navn . $epost . $telefon . $emne)) {
    svar(400, 'Ugyldig innhold.');
}

// Spamheuristikk. Bevisst romslig — vi vil heller slippe gjennom én spam enn
// å avvise en ekte kunde.
$lenker = preg_match_all('#https?://#i', $melding);
if ($lenker > 2) {
    svar(422, 'Meldingen inneholder for mange lenker. Skriv gjerne uten lenker, så tar vi kontakt.');
}
if (preg_match('#https?://#i', $navn)) {
    svar(422, 'Ugyldig navn.');
}
// Meldinger helt uten mellomrom er maskingenerert
if (mb_strlen($melding) > 40 && !str_contains($melding, ' ')) {
    svar(422, 'Ugyldig innhold.');
}

// --- Sending -----------------------------------------------------------------
// From må være en adresse på eget domene for å passere SPF. Besøkendes adresse
// legges i Reply-To, slik at «svar» i e-postklienten går rett til vedkommende.
$emne_trygt = $emne !== '' ? $emne : 'Henvendelse fra nettsiden';
$overskrift = sprintf('[idebolig.no] %s — %s', $emne_trygt, $navn);

$linjer = [
    'Ny henvendelse fra kontaktskjemaet på idebolig.no',
    str_repeat('-', 52),
    '',
    'Navn:     ' . $navn,
    'E-post:   ' . $epost,
    'Telefon:  ' . ($telefon !== '' ? $telefon : '(ikke oppgitt)'),
    'Gjelder:  ' . $emne_trygt,
    '',
    'Melding:',
    $melding,
    '',
    str_repeat('-', 52),
    'Sendt: ' . date('d.m.Y H:i'),
];
$kropp = implode("\n", $linjer);

$hoder = implode("\r\n", [
    'From: Idébolig nettside <' . $avsender . '>',
    'Reply-To: ' . $navn . ' <' . $epost . '>',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'X-Mailer: idebolig-skjema',
]);

$sendt = mail(
    $mottaker,
    '=?UTF-8?B?' . base64_encode($overskrift) . '?=',
    $kropp,
    $hoder,
    '-f' . $avsender
);

if (!$sendt) {
    error_log('skjema.php: mail() feilet for ' . $epost);
    svar(500, 'Vi klarte ikke å sende meldingen. Prøv igjen, eller ring oss på 91 92 66 66.');
}

svar(200, 'Takk for henvendelsen! Vi svarer normalt innen én virkedag.', true);
