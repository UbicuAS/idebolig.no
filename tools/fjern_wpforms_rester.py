# -*- coding: utf-8 -*-
"""
Fjerner WPForms- og Google-rester som ikke lenger har noe å gjøre på siden.

Kontaktskjemaet (IB1.11) er vårt eget: `ibk2-skjema`, med egen validering og
Cloudflare Turnstile, som sender til skjema.php. WPForms-skjemaet det erstattet
er borte fra markeringen, men speilingen tok med seg alle filene det lastet.

Det står igjen tre ting, og det tredje er det alvorlige:

  1. WPForms' egne filer — ni JS-filer og to stilark, til sammen rundt 680 KB
     på nettopp den siden en kunde bruker for å ta kontakt. De gjør ingenting;
     det finnes ikke et WPForms-skjema å betjene.

  2. Site Kit-skriptet `googlesitekit-events-provider-wpforms`, som ligger på
     alle 17 sider. Sporingen fra Site Kit ble fjernet i IB1.3 — dette er en
     rest som ble stående.

  3. Googles reCAPTCHA. WPForms lastet `www.google.com/recaptcha/api.js`, og
     den laster i sin tur et skript til fra gstatic.com. Målt i nettleser:
     `grecaptcha` er faktisk til stede som objekt. Altså to kall til Google
     for hver besøkende på kontaktsiden — på en side der Turnstile ble valgt
     framfor nettopp reCAPTCHA for å holde Google borte og slippe
     samtykkekrav. Skjemaet vårt bruker den ikke.

Vårt eget skjema rører ikke noe av dette: det har egen validering, og laster
Turnstile selv. Kontrollert før fjerning.

Kjøres fra rotmappen:  python tools/fjern_wpforms_rester.py
"""
import glob
import re
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent

# Tagger med id som hører til WPForms, Site Kit eller reCAPTCHA.
#
# <link> og <script> må ha hver sin regel. Ett felles uttrykk med en
# «enten /> eller …</script>»-veksling ser riktig ut, men på et <link ... />
# spiser den grådige [^>]* skråstreken, /> feiler, og vekslingen faller
# gjennom til </script>-grenen — som da sluker alt fram til neste
# </script> lenger nede i dokumentet. Det tok med seg jQuery og halve
# Elementor første gang skriptet kjørte.
ID = r'\bid=["\'](?:wpforms|googlesitekit)[^"\']*["\']'
LENKE = re.compile(r'<link\b[^>]*' + ID + r'[^>]*>\n?')
SKRIPT = re.compile(r'<script\b[^>]*' + ID + r'[^>]*>(?:(?!</script>).)*</script>\n?', re.S)

# Innstillingsblokken har ingen gjenkjennelig id — den finnes på innholdet.
INNSTILLINGER = re.compile(
    r'<script\b(?:(?!</script>).)*wpforms_settings(?:(?!</script>).)*</script>\n?',
    re.S,
)

endret = 0
filer = ["index.html", "edvard.html"] + sorted(glob.glob("*/index.html", root_dir=ROT))
for rel in filer:
    fil = ROT / rel
    if not fil.exists():
        continue

    rådata = fil.read_bytes()
    crlf = b"\r\n" in rådata
    tekst = rådata.decode("utf-8").replace("\r\n", "\n")

    ny, n1 = LENKE.subn("", tekst)
    ny, n2 = SKRIPT.subn("", ny)
    ny, n3 = INNSTILLINGER.subn("", ny)
    n1 += n2

    if ny == tekst:
        continue

    # Sikring mot nettopp den feilen som ble gjort første gang: alt utenom
    # WPForms/Site Kit skal stå igjen. jQuery og Elementor er kanarifuglene —
    # forsvinner de, har uttrykket spist for mye.
    for vakt in ("ibk2-form", "jquery.min.js", "elementor/assets/js/frontend.min.js"):
        if vakt in tekst and vakt not in ny:
            raise SystemExit("STOPP: %s ble fjernet fra %s" % (vakt, rel))

    fil.write_bytes((ny.replace("\n", "\r\n") if crlf else ny).encode("utf-8"))
    endret += 1
    spart = (len(tekst) - len(ny)) / 1024.0
    print("%-26s %2d tagger, %2d innstillingsblokk, %.1f KB markering" % (rel, n1, n3, spart))

print("\n%d filer endret" % endret)
