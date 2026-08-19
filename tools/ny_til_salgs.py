# -*- coding: utf-8 -*-
"""
Lager siden /til-salgs/ og legger «Til salgs» inn i menyene på alle sider.

Marius ba 19. aug om en egen fane for fremtidige salgsprosjekter. Innhold
finnes ikke ennå, så siden er en plassholder i sidens eget stilspråk (samme
palett og kicker-mønster som /prosjekter/): «Her kommer fremtidige prosjekter
for salg», med veier videre til kontaktsiden og boligmodellene.

Skriptet gjør tre ting, alle idempotente:

  1. SIDEN bygges av skallet til prosjekter/index.html: alt innenfor <main>
     byttes med plassholderseksjonen, tittel/metabeskrivelse/canonical settes,
     og prosjekter-sidens «current menu»-markering nøytraliseres.
  2. HOVEDMENYEN får «Til salgs» før Kontakt-punktet på alle sider (begge
     menykopiene), etter samme mønster som tools/meny_boligkatalog.py — men
     CRLF-trygt, i motsetning til originalen.
  3. MOBILMENYEN (det egne panelet fra tools/fiks_mobilmeny.py) får
     ['Til salgs','til-salgs/'] inn i PUNKTER-listen på alle sider.

Vakter: antallet <link>-, <script>- og <style>-tagger skal være uendret av
menyendringene, og «Til salgs» skal forekomme nøyaktig tre ganger per side
(to menykopier + mobilpanelet). Fila skrives ikke hvis noe annet skjer.

CRLF: filene er sjekket ut med CRLF. Les binært, arbeid med LF, skriv tilbake
med opprinnelig linjeslutt.

Kjøres fra rotmappen:  python tools/ny_til_salgs.py
"""
import re
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
MARKOR = "ib-meny-til-salgs"

TITTEL = "<title>Til salgs &#8211; kommende prosjekter &#8211; Idébolig AS</title>"
BESKRIVELSE = ('<meta name="description" content="Her legger vi ut fremtidige '
               "prosjekter for salg fra Idébolig. Ingen boliger ligger ute akkurat "
               'nå – ta kontakt, så gir vi deg beskjed når noe kommer.">')
CANONICAL = "https://idebolig.no/til-salgs/"

SEKSJON = """<style>
#ibs{--gull:#C99C55;--mork:#33302C;--grå:#6b6257;--krem:#F7F3EC;
  font-family:Poppins,sans-serif;color:var(--mork);background:var(--krem);
  padding:88px 20px 110px}
:where(#ibs *){box-sizing:border-box;margin:0}
.ibs-indre{max-width:760px;margin:0 auto}
.ibs-kicker{display:flex;align-items:center;gap:14px;font:600 12px/1 Inter,sans-serif;
  letter-spacing:.24em;text-transform:uppercase;color:var(--gull);margin-bottom:22px}
.ibs-kicker::after{content:"";flex:0 0 46px;height:1px;background:var(--gull);opacity:.55}
#ibs h1{font-size:clamp(34px,4.5vw,52px);font-weight:700;line-height:1.14;
  letter-spacing:-.015em;margin-bottom:20px}
.ibs-intro{color:var(--grå);font-size:17px;line-height:1.8;margin-bottom:44px}
.ibs-kort{background:#fff;border:1px solid #ece5d9;border-radius:14px;
  padding:40px 36px;box-shadow:0 10px 30px rgba(51,48,44,.06)}
.ibs-kort h2{font-size:21px;font-weight:600;margin-bottom:12px}
.ibs-kort p{color:var(--grå);font-size:15.5px;line-height:1.75;margin-bottom:26px}
.ibs-knapper{display:flex;flex-wrap:wrap;gap:14px;align-items:center}
.ibs-knapp{display:inline-block;background:var(--gull);color:#fff;font:600 14px/1 Poppins,sans-serif;
  letter-spacing:.02em;padding:15px 28px;border-radius:8px;text-decoration:none;
  transition:background .18s}
.ibs-knapp:hover,.ibs-knapp:focus{background:#b5883f;color:#fff}
.ibs-lenke{color:var(--mork);font:500 14px/1 Poppins,sans-serif;text-decoration:none;
  border-bottom:1px solid var(--gull);padding-bottom:3px}
.ibs-lenke:hover,.ibs-lenke:focus{color:var(--gull)}
</style>
<section id="ibs">
 <div class="ibs-indre">
  <p class="ibs-kicker">Kommer for salg</p>
  <h1>Til salgs</h1>
  <p class="ibs-intro">Her legger vi ut fremtidige prosjekter for salg.
   Akkurat nå har vi ingen boliger ute i markedet &#8212; men det kommer.</p>
  <div class="ibs-kort">
   <h2>Vil du få beskjed først?</h2>
   <p>Fortell oss hva du ser etter, så tar vi kontakt når vi har et prosjekt
    på vei ut i markedet. I mellomtiden kan du se boligmodellene vi bygger.</p>
   <div class="ibs-knapper">
    <a class="ibs-knapp" href="../kontakt/">Ta kontakt</a>
    <a class="ibs-lenke" href="../v%C3%A5re-boliger/">Se boligmodellene våre</a>
   </div>
  </div>
 </div>
</section>
"""

# Menyfeltet i sidehodet er 60 % bredt og rommet nøyaktig fem punkter. Med
# «Til salgs» som sjette punkt brøt «Kontakt» ned på egen linje på vanlige
# skjermbredder. Logobildet er 308 px i en 430 px boks, så skillet flyttes fra
# 40/60 til 36/64 — og i det trange båndet 1025–1220 px (der Elementors
# nettbrettoppsett IKKE gjelder, det tar over først under 1025 px) strammes
# menyen i tillegg med mindre skrift og marger. Målt i nettleser på 1025,
# 1050, 1221, 1280 og 1440 px: alle seks punktene på én linje, logo urørt
# fra 1221 px og oppover.
MENYSTIL_ID = "ib-meny-plass"
MENYSTIL = (
    '<style id="' + MENYSTIL_ID + '">\n'
    "/* Plass til sjette menypunkt — se tools/ny_til_salgs.py. NB: ordlyden\n"
    "   her må ikke inneholde menypunktets navn, det telles av en vakt. */\n"
    "@media (min-width:1025px){"
    ".elementor-1253 .elementor-element.elementor-element-5f08d62b{--width:36%}"
    ".elementor-1253 .elementor-element.elementor-element-6834729c{--width:64%}}\n"
    "@media (min-width:1025px) and (max-width:1220px){"
    ".elementor-1253 .elementor-element.elementor-element-5f08d62b{--width:30%}"
    ".elementor-1253 .elementor-element.elementor-element-6834729c{--width:70%}"
    ".elementor-1253 .elementor-nav-menu a.elementor-item{font-size:14px!important;margin-right:8px!important}}\n"
    "</style>\n")
MENYSTIL_RE = re.compile(r'<style id="' + MENYSTIL_ID + r'">.*?</style>\n?', re.S)

TITTEL_RE = re.compile(r"<title>[^<]*</title>")
CANONICAL_RE = re.compile(r'(<link rel=["\']canonical["\'][^>]*href=["\'])([^"\']+)(["\'])')
BESKRIVELSE_RE = re.compile(r'<meta name="description" content="[^"]*">')
# Matcher på lenketeksten, ikke href-en: på kontaktsiden peker Kontakt-punktet
# på «index.html» (aria-current), så et href-mønster bommer der — det er samme
# grunn til at meny_boligkatalog.py i sin tid hoppet over kontaktsiden.
KONTAKT_LI = re.compile(
    r'(<li[^>]*class="menu-item[^"]*"[^>]*>\s*<a[^>]*class="elementor-item[^"]*"[^>]*>\s*Kontakt</a>)')
MOBIL_KONTAKT = "  ['Kontakt','kontakt/']"
MOBIL_NYTT = "  ['Til salgs','til-salgs/'],\n"


def les(fil):
    rå = fil.read_bytes()
    return rå.decode("utf-8").replace("\r\n", "\n"), b"\r\n" in rå


def skriv(fil, tekst, crlf):
    ut = tekst.replace("\n", "\r\n") if crlf else tekst
    fil.write_bytes(ut.encode("utf-8"))


def telling(tekst):
    return {t: tekst.count(t) for t in ("<link", "<script", "</script>", "<style", "</head>")}


def bygg_siden():
    """Bygger til-salgs/index.html av prosjekter-skallet. Returnerer True ved endring."""
    skall, crlf = les(ROT / "prosjekter" / "index.html")

    start = re.search(r"<main[^>]*>", skall)
    slutt = skall.find("</main>")
    if not start or slutt < 0:
        raise SystemExit("STOPP: fant ikke <main>-elementet i prosjekter/index.html")
    side = skall[: start.end()] + "\n" + SEKSJON + skall[slutt:]

    if len(TITTEL_RE.findall(side)) != 1:
        raise SystemExit("STOPP: fant ikke nøyaktig én <title> i skallet")
    side = TITTEL_RE.sub(TITTEL, side, count=1)
    side = BESKRIVELSE_RE.sub("", side)
    side = side.replace(TITTEL + "\n", TITTEL + "\n" + BESKRIVELSE + "\n", 1)
    if BESKRIVELSE not in side:
        raise SystemExit("STOPP: fikk ikke satt inn metabeskrivelsen")
    if not CANONICAL_RE.search(side):
        raise SystemExit("STOPP: fant ikke canonical i skallet")
    side = CANONICAL_RE.sub(lambda m: m.group(1) + CANONICAL + m.group(3), side, count=1)

    # Prosjekter-sidens menymarkering skal ikke arves — verken li-klassene,
    # ankerets elementor-item-active eller aria-current.
    for klasse in ("current-menu-item", "current_page_item", "current-menu-ancestor",
                   "current_page_ancestor", "current_page_parent", "elementor-item-active"):
        side = side.replace(" " + klasse, "")
    side = side.replace(' aria-current="page"', "")

    # Skallet er én mappe dypt, det er den nye siden også — stiene stemmer.
    for merke in ("elementor-frontend-js", "ib-mobilmeny", "jquery.min.js"):
        if merke not in side:
            raise SystemExit("STOPP: «%s» forsvant fra den nye siden" % merke)

    mål = ROT / "til-salgs" / "index.html"
    gammel = mål.read_bytes().decode("utf-8").replace("\r\n", "\n") if mål.exists() else None
    if gammel == side:
        return False
    mål.parent.mkdir(exist_ok=True)
    skriv(mål, side, crlf)
    return True


def oppdater_menyer():
    """«Til salgs» inn i hoved- og mobilmeny på alle sider. Returnerer antall endret."""
    endret = 0
    for fil in sorted(ROT.rglob("*.html")):
        rel = fil.relative_to(ROT)
        if rel.parts[0] in ("wp-content", "wp-includes", "tools", "prosjekt-assets"):
            continue
        if fil.name.startswith("._"):
            continue
        tekst, crlf = les(fil)
        if "<nav" not in tekst:
            continue
        for_ = tekst
        telling_for = telling(tekst)

        # Hovedmenyen: fjern ev. gammel variant, sett inn før hvert Kontakt-punkt.
        tekst = re.sub(r"<li[^>]*" + MARKOR + r"[^>]*>.*?</li>", "", tekst)
        prefix = "../" * (len(rel.parts) - 1)
        nytt_li = ('<li class="menu-item menu-item-type-post_type menu-item-object-page %s">'
                   '<a href="%stil-salgs/" class="elementor-item menu-link">Til salgs</a></li>'
                   % (MARKOR, prefix))
        tekst, antall_li = KONTAKT_LI.subn(nytt_li + r"\1", tekst)
        if antall_li == 0:
            print("STOPP  %s: fant ikke Kontakt-punktet i hovedmenyen" % rel)
            raise SystemExit(1)

        # Mobilmenyen: inn i PUNKTER-listen hvis panelet finnes på siden.
        # På selve til-salgs-siden står «Til salgs» også i tittelen og H1-en.
        forventet = antall_li + (2 if rel.parts[0] == "til-salgs" else 0)
        if "ib-mobilmeny" in tekst:
            if "'til-salgs/'" not in tekst:
                if MOBIL_KONTAKT not in tekst:
                    print("STOPP  %s: fant ikke Kontakt i mobilmenyens PUNKTER" % rel)
                    raise SystemExit(1)
                tekst = tekst.replace(MOBIL_KONTAKT, MOBIL_NYTT + MOBIL_KONTAKT, 1)
            forventet += 1

        if tekst.count("Til salgs") != forventet:
            print("STOPP  %s: «Til salgs» står %d ganger, ventet %d — skriver ikke"
                  % (rel, tekst.count("Til salgs"), forventet))
            raise SystemExit(1)
        if telling(tekst) != telling_for:
            print("STOPP  %s: tagg-tellingen endret seg — skriver ikke" % rel)
            raise SystemExit(1)

        if tekst != for_:
            skriv(fil, tekst, crlf)
            endret += 1
            print("%-28s meny oppdatert (%d hovedmeny + %s mobil)"
                  % (rel, antall_li, "1" if forventet > antall_li else "0"))
        else:
            print("%-28s uendret" % rel)
    return endret


def legg_inn_menystil():
    """Stilblokken som gir plass til sjette menypunkt, sist i <body> på alle
    sider med meny. Returnerer antall endret."""
    endret = 0
    for fil in sorted(ROT.rglob("*.html")):
        rel = fil.relative_to(ROT)
        if rel.parts[0] in ("wp-content", "wp-includes", "tools", "prosjekt-assets"):
            continue
        if fil.name.startswith("._"):
            continue
        tekst, crlf = les(fil)
        if "<nav" not in tekst or "</body>" not in tekst:
            continue
        for_ = tekst
        tekst = MENYSTIL_RE.sub("", tekst)
        tekst = tekst.replace("</body>", MENYSTIL + "</body>", 1)
        if tekst.count(MENYSTIL_ID) != 1 or tekst.count("</body>") != for_.count("</body>"):
            print("STOPP  %s: stilblokken landet feil — skriver ikke" % rel)
            raise SystemExit(1)
        if tekst != for_:
            skriv(fil, tekst, crlf)
            endret += 1
    return endret


ny = bygg_siden()
print("til-salgs/index.html %s\n" % ("bygget" if ny else "uendret"))
print("%d sider fikk menystil\n" % legg_inn_menystil())
n = oppdater_menyer()
print("\n%d sider fikk menyendring" % n)
