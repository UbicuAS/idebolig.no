<?php
/**
 * MAL — kopier denne til webhotellet som ~/skjema-config.php
 * altså ETT NIVÅ OVER /www, slik at den aldri kan hentes over nett.
 *
 * Denne fila skal aldri inneholde ekte nøkler i git. Den ekte fila ligger
 * kun på serveren, med rettigheter 600.
 *
 *   scp skjema-config.php idebolig@login.domeneshop.no:~/skjema-config.php
 *   ssh idebolig@login.domeneshop.no 'chmod 600 ~/skjema-config.php'
 */

return [
    // Hvem henvendelsene skal til.
    'mottaker' => 'post@idebolig.no',

    // Avsenderadresse. MÅ ligge på idebolig.no for å passere SPF — bruker vi
    // den besøkendes egen adresse her, blir e-posten stemplet som forfalskning
    // og havner i søppelpost.
    //
    // Vi bruker post@idebolig.no, som allerede finnes. Å opprette en egen
    // avsenderadresse ville vært en endring i kundens e-postoppsett, og det
    // skal vi ikke gjøre. Besøkendes adresse havner i Reply-To.
    'avsender' => 'post@idebolig.no',

    // Secret key fra Turnstile-widgeten i Cloudflare (IKKE site key —
    // den er offentlig og ligger i HTML-en).
    'turnstile_secret' => 'SETT_INN_SECRET_KEY_HER',

    // Hvor telleren for rate-limiting lagres. Utenfor webroten.
    'loggmappe' => __DIR__ . '/skjema-logg',

    // Maks antall innsendinger per IP per time.
    'maks_per_time' => 5,
];
