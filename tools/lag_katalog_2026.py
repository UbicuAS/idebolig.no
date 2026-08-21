#!/usr/bin/env python3
"""Bygger den store bla-katalogen «Boligkatalog 2026» på en skjult URL
(/katalog-2026-h7vq3kfm/) — inspirert av arkitekt-hus.no sin Heyzine-katalog,
men selvhostet.

Bla-motoren er StPageFlip (page-flip.browser.js, MIT, vendret i katalogmappa)
— den gir myk sidebøy, dra-fra-hjørnet, skygger og stiv perm/myke ark, altså
den ekte katalogfølelsen. (Første utgave brukte den stive rotateY-motoren fra
/boligkatalog/; byttet 21. aug etter tilbakemelding fra Marius.)

Innhold: hard forside → velkomst + innholdsfortegnelse → to oppslag per bolig
(fasade + fakta, interiør + plantegning) → prosess, guide, tjenester,
tilpasning, kontakt og QR → hard bakside. Alle åtte modellene har ekte
plantegninger; plassholder() står igjen som reserve for nytt innhold.

Siden er med vilje utenfor sitemap.xml og menyen, og har noindex/nofollow.
Sideskall (header/footer) hentes fra våre-boliger/index.html. Idempotent.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nytt_boligkatalog import BOLIGER, beste_bilde, IKON  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ARKIV = Path(__file__).resolve().parent / "original-main"
SLUG = "katalog-2026-h7vq3kfm"   # skjult URL — endres slugen, endres lenken
UP = "wp-content/uploads"

# Ekstra bildepar til interiør-/fasadesiden per bolig: (bildetekst, stamme).
# Stammene finnes i wp-content/uploads og løses av beste_bilde().
MEDIA = {
    "alva":         [("Kjøkken", f"{UP}/2025/04/Kjokken"),
                     ("Stue", f"{UP}/2025/04/Stue")],
    "edvard":       [("Kjøkken", f"{UP}/2024/11/Kjokken"),
                     ("Stue", f"{UP}/2024/11/Stue-ny-dag")],
    "edvard-prakt": [("Kjøkken", f"{UP}/2025/03/Kjokken-2"),
                     ("Stue", f"{UP}/2025/03/Stue-2")],
    "embla":        [("Fasade, bakside", f"{UP}/2025/04/Fasade-bakside-1"),
                     ("Fasade, framside", f"{UP}/2025/04/Fasade-fremside")],
    "nora":         [("Spisestue", f"{UP}/2024/11/Spisestue-post-prod"),
                     ("Fasade, bakside", f"{UP}/2024/11/Fasade-bakside-Nora")],
    "odin":         [("Fasade", f"{UP}/2024/11/Fasade-fremside-post-prod-1"),
                     ("Fasade, bakside", f"{UP}/2024/11/Fasade-bakside-post-prod")],
    "tiril":        [("Kjøkken", f"{UP}/2025/06/Kjokken"),
                     ("Stue", f"{UP}/2025/06/Stue")],
    "vilde":        [("Stue", f"{UP}/2025/05/Stue-Vilde-scaled"),
                     ("Soverom", f"{UP}/2025/05/Soverom-Vilde")],
}

# Ekte plantegninger der de finnes; alle andre får plassholder.
# Stier som starter med "planer/" ligger i katalogmappa (egenproduserte
# møblerte 2D-planer); andre er stammer i wp-content som løses av beste_bilde.
PLANER = {
    "vilde": [("3D-plantegning", f"{UP}/2025/05/Vilde-3d-plan"),
              ("3D-plantegning, alternativ", f"{UP}/2025/05/Vilde-3d-plan-hus-2")],
    "edvard-prakt": [("U. etasje — utleiedel 47 m² + kjeller", "planer/edvard-prakt-uetasje.svg"),
                     ("1. etasje", "planer/edvard-prakt-1etasje.svg"),
                     ("2. etasje", "planer/edvard-prakt-2etasje.svg")],
    # Edvard = samme hus uten sokkel (beskjed fra Marius 21.08.2026)
    "edvard": [("1. etasje", "planer/edvard-1etasje.svg"),
               ("2. etasje", "planer/edvard-2etasje.svg")],
    "alva": [("1. etasje", "planer/alva-1etasje.svg"),
             ("2. etasje", "planer/alva-2etasje.svg")],
    "embla": [("1. etasje — to leiligheter", "planer/embla-1etasje.svg"),
              ("2. etasje — to leiligheter", "planer/embla-2etasje.svg")],
    "odin": [("1. etasje", "planer/odin-1etasje.svg"),
             ("2. etasje", "planer/odin-2etasje.svg")],
    "nora": [("1. etasje", "planer/nora-1etasje.svg"),
             ("2. etasje", "planer/nora-2etasje.svg")],
    # Tiril er tegnet fra målsatt PDF (begge etasjer, begge enheter).
    "tiril": [("1. etasje — begge enhetene", "planer/tiril-1etasje.svg"),
              ("2. etasje — begge enhetene", "planer/tiril-2etasje.svg")],
}


def bildesrc(stem: str) -> str:
    return stem if stem.startswith("planer/") else beste_bilde(stem)


# Tre salgspunkter per modell — kun forhold som er dokumentert i
# spesifikasjonene/tegningene (ingen dikting av fakta).
HIGHLIGHTS = {
    "alva": ["Terrasse og balkong langs hele hovedfasaden",
             "Åpen stue- og kjøkkenløsning mot terrassen",
             "Fem soverom og tre bad"],
    "edvard": ["Dobbel garasje med takterrasse over",
               "Fem soverom fordelt på to etasjer",
               "Klassisk uttrykk med moderne planløsning"],
    "edvard-prakt": ["Utleiedel på 47 m² i sokkeletasjen",
                     "Takterrasse på 42,7 m² over dobbelgarasjen",
                     "Kjellerstue og rikelig med bodplass"],
    "embla": ["Fire leiligheter på 84 m² hver",
              "Felles inngang med trapp og heis",
              "Egen terrasse eller balkong til hver leilighet"],
    "nora": ["310 m² med plass til hele familien",
             "Fire soverom og to bad",
             "Klassisk arkitektur med gjennomtenkte detaljer"],
    "odin": ["Kompakt og arealeffektiv planløsning",
             "Fire soverom og to praktiske boder",
             "Sjarmerende og lettstelt hjem"],
    "tiril": ["To romslige enheter på 176 m² hver",
              "Garasje til hver enhet",
              "Moderne uttrykk over to etasjer"],
    "vilde": ["Hypermoderne funkisuttrykk",
              "Fem soverom og dobbel garasje",
              "Store vindusflater og lyse rom"],
}

PROSESS = [
    ("Første møte og tomtebefaring",
     "Vi blir kjent med ønskene deres og vurderer tomtens muligheter — "
     "utsikt, solforhold og grunnforhold."),
    ("Tegninger og tilpasning",
     "Boligmodellen tilpasses tomten og behovene deres — eller vi tegner "
     "helt nytt sammen med dere."),
    ("Pristilbud og avtale",
     "Dere får et skriftlig pristilbud, og vi avtaler leveranseomfang og "
     "fremdrift før noe settes i gang."),
    ("Byggesøknad",
     "Vi håndterer byggesøknad, nabovarsel og dialogen med kommunen, og "
     "holder dere oppdatert underveis."),
    ("Prosjektering",
     "Arbeidstegninger og tekniske planer utarbeides, slik at alle fag "
     "vet nøyaktig hva som skal bygges."),
    ("Grunnarbeid",
     "Vi utfører graving, grunnarbeid og betongfundamentering — fra "
     "byggegrop til ferdig støpt fundament."),
    ("Byggeperioden",
     "Montasje og utførelse med faste kontrollpunkter, fra tett bygg til "
     "ferdige overflater."),
    ("Ferdigbefaring",
     "Boligen gjennomgås grundig sammen med dere. Eventuelle avvik "
     "protokollføres og utbedres."),
    ("Overtakelse",
     "Formell overtakelse med dokumentasjon av boligen — og nøklene til "
     "deres nye hjem."),
    ("Oppfølging",
     "Vi følger opp etter innflytting, slik at dere er trygge på boligen "
     "også etter at dere har flyttet inn."),
]

GUIDE = [
    ("Budsjett",
     "Avklar rammene tidlig. Ulike modeller har ulik pris, og tilpasninger "
     "påvirker totalen. Et tydelig budsjett gjør alle valg enklere."),
    ("Tomt og beliggenhet",
     "Tomtens form, helning og solforhold påvirker hvilken modell som "
     "passer. En smal tomt kan peke mot to etasjer; en flat og romslig "
     "tomt gir flere muligheter."),
    ("Livssituasjon og behov",
     "Tenk fem–ti år frem: Trenger dere flere soverom, hjemmekontor eller "
     "utleiedel? Velg en bolig som vokser med dere."),
    ("Stil og uttrykk",
     "Klassisk eller funkis? Boligen bør både speile smaken deres og passe "
     "inn i omgivelsene. Flere av modellene finnes i ulike uttrykk."),
    ("Energi og drift",
     "Kompakte boliger er enklere å varme opp. Tenk også på muligheten for "
     "solceller og andre energiløsninger når dere velger."),
    ("Verdi over tid",
     "En gjennomarbeidet bolig med fleksibel planløsning holder seg "
     "attraktiv — også den dagen dere eventuelt skal selge."),
]


# Frisiden (s. 45): hva som faktisk kan endres på en modell.
TILPASNING = [
    ("Planløsningen",
     "Flytt en vegg, slå sammen to soverom eller gjør om et soverom til "
     "hjemmekontor. Bærende konstruksjon setter rammene — innenfor dem er "
     "det mye som lar seg justere."),
    ("Garasje, bod og uteplass",
     "Garasje kan legges til, gjøres dobbel eller trekkes inn i boligen. "
     "Edvard, Edvard Prakt og Vilde har dobbel garasje allerede i "
     "grunnutgaven."),
    ("Utleiedel",
     "Edvard Prakt har en utleiedel på 30 m². Vurderer dere utleie i en "
     "annen modell, ser vi på om planløsningen kan legges til rette for en "
     "egen enhet."),
    ("Uttrykk og materialer",
     "Kledning, farger, takform og vindusinndeling avgjør om boligen leser "
     "klassisk eller moderne. Samme planløsning kan få svært ulikt uttrykk."),
    ("Speilvending og tomt",
     "Modellen kan speilvendes slik at stue og uteplass vender mot sola og "
     "utsikten, og tilpasses fall, adkomst og himmelretning på tomten."),
]

def qr_svg(url: str = "https://idebolig.no/", storrelse: int = 340) -> str:
    """QR-kode som inline-SVG (genereres med segno ved bygging)."""
    import segno
    qr = segno.make(url, error="m")
    matrise = [[bool(m) for m in rad] for rad in qr.matrix]
    n = len(matrise)
    d = []
    for y, rad in enumerate(matrise):
        for x, mork in enumerate(rad):
            if mork:
                d.append(f"M{x} {y}h1v1h-1z")
    return (f'<svg class="fb-qr" viewBox="-2 -2 {n + 4} {n + 4}" '
            f'width="{storrelse}" height="{storrelse}" '
            f'xmlns="http://www.w3.org/2000/svg">'
            f'<rect x="-2" y="-2" width="{n + 4}" height="{n + 4}" fill="#FDFBF7" rx="2"/>'
            f'<path d="{"".join(d)}" fill="#33302C"/></svg>')


def avsnitt(slug: str) -> list[str]:
    """Alle innholdsavsnitt fra boligsidens originaltekst."""
    kilde = (ARKIV / f"{slug}.html").read_text(encoding="utf-8")
    ut = []
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", kilde, re.S):
        txt = re.sub(r"<[^>]+>", " ", m.group(1))
        txt = re.sub(r"\s+", " ", txt).strip()
        if len(txt) > 60:
            ut.append(txt)
    return ut


def kutt(txt: str, maks: int) -> str:
    if len(txt) <= maks:
        return txt
    return txt[:maks].rsplit(" ", 1)[0].rstrip(",.;:") + " …"


def plassholder(tittel: str, tekst: str) -> str:
    return f"""<div class="fb-ph">
      <span class="fb-ph-chip">Plassholder</span>
      <b>{tittel}</b>
      <p>{tekst}</p>
    </div>"""


def fotoside(stem: str, navn: str, nr: int) -> str:
    return (f'<div class="fb-foto"><img src="{beste_bilde(stem)}" alt="{navn}">'
            f'<p>{navn}</p><span class="fb-sidenr fb-sidenr--v">{nr}</span></div>')


def infoside(b: dict, nr: int) -> str:
    bra = f'{b["bra"]} m²' + (" pr enhet" if b["braenhet"] else "")
    specs = [("BRA", bra), ("Soverom", str(b["sov"])), ("Bad", str(b["bad"]))]
    if b["garasje"]:
        specs.append(("Garasje", b["garasje"]))
    if b["utleie"]:
        specs.append(("Utleiedel", b["utleie"]))
    spec_html = "".join(f'<div class="fb-spec"><span>{k}</span><b>{v}</b></div>'
                        for k, v in specs)
    avsn = avsnitt(b["slug"])
    tekst = kutt(" ".join(avsn[:2]), 430) if avsn else ""
    hl = "".join(f"<li>{p}</li>" for p in HIGHLIGHTS.get(b["slug"], []))
    return f"""<div class="fb-info">
      <p class="fb-kicker">{b['type']} · {b['stil']}</p>
      <h3>{b['navn']}</h3>
      <p class="fb-tagline">{b['tagline']}</p>
      <div class="fb-specs">{spec_html}</div>
      <ul class="fb-hl">{hl}</ul>
      <p class="fb-tekst">{tekst}</p>
      <a class="fb-lenke" href="../{b['slug']}/">Se boligen på nettsiden →</a>
      <span class="fb-sidenr fb-sidenr--h">{nr}</span>
    </div>"""


def duoside(par: list, nr: int) -> str:
    """To bilder over hverandre med bildetekst."""
    figs = "".join(
        f'<figure><img src="{beste_bilde(stem)}" alt="{navn}">'
        f'<figcaption>{navn}</figcaption></figure>'
        for navn, stem in par[:2])
    return (f'<div class="fb-duo">{figs}'
            f'<span class="fb-sidenr fb-sidenr--v">{nr}</span></div>')


def planfigurer(planer: list, navn: str) -> str:
    figs = "".join(
        f'<figure class="fb-planfig"><img src="{bildesrc(stem)}" alt="{tittel} — {navn}">'
        f'<figcaption>{tittel}</figcaption></figure>'
        for tittel, stem in planer)
    return f'<div class="fb-planer">{figs}</div>'


def planside(b: dict, nr: int) -> str:
    avsn = avsnitt(b["slug"])
    mer = kutt(" ".join(avsn[1:3]), 330) if len(avsn) > 1 else ""
    if b["slug"] in PLANER:
        indre = planfigurer(PLANER[b["slug"]], b["navn"])
    else:
        indre = plassholder(f"Plantegninger — {b['navn']}",
                            "Legges inn senere, f.eks. 1. og 2. etasje.")
    return f"""<div class="fb-info">
      <p class="fb-kicker">{b['navn']}</p>
      <h3>Plantegning</h3>
      {indre}
      <p class="fb-tekst fb-tekst--kort">{mer}</p>
      <span class="fb-sidenr fb-sidenr--h">{nr}</span>
    </div>"""


def plansider(b: dict, nr_v: int, nr_h: int) -> tuple[str, str]:
    """Boliger med 3+ plantegninger får et helt planoppslag (begge sider)."""
    planer = PLANER[b["slug"]]
    venstre = f"""<div class="fb-info">
      <p class="fb-kicker">{b['navn']}</p>
      <h3>Plantegninger</h3>
      {planfigurer(planer[:2], b['navn'])}
      <span class="fb-sidenr fb-sidenr--h fb-sidenr--vs">{nr_v}</span>
    </div>"""
    avsn = avsnitt(b["slug"])
    mer = kutt(" ".join(avsn[1:3]), 300) if len(avsn) > 1 else ""
    høyre = f"""<div class="fb-info">
      <p class="fb-kicker">{b['navn']}</p>
      <h3>&nbsp;</h3>
      {planfigurer(planer[2:], b['navn'])}
      <p class="fb-tekst fb-tekst--kort">{mer}</p>
      <span class="fb-sidenr fb-sidenr--h">{nr_h}</span>
    </div>"""
    return venstre, høyre


def velkomstside(nr: int) -> str:
    return f"""<div class="fb-info">
      <p class="fb-kicker">Velkommen</p>
      <h3>Skap drømmeboligen sammen med Idébolig</h3>
      <p class="fb-brod">Å bygge bolig er en av de største beslutningene du
        tar. I denne katalogen finner du våre åtte boligmodeller — fra
        kompakte klassikere til moderne funkis — sammen med det du trenger å
        vite om veien fra idé til innflytting.</p>
      <p class="fb-brod">Hver modell er tegnet med omtanke for norske forhold
        og norsk byggeskikk, og kan tilpasses din tomt, dine behov og ditt
        budsjett. Du får ett kontaktpunkt hele veien: tegninger, byggesøknad,
        prosjektering, grunnarbeid og utførelse.</p>
      <p class="fb-brod">Bla deg gjennom, la deg inspirere — og ta kontakt
        når du finner boligen du vil se nærmere på.</p>
      <p class="fb-sign">Idébolig AS · Hamar</p>
      <span class="fb-sidenr fb-sidenr--h fb-sidenr--vs">{nr}</span>
    </div>"""


def omossside(nr: int) -> str:
    return f"""<div class="fb-info">
      <p class="fb-kicker">Om Idébolig</p>
      <h3>Unike hjem, bygget for å vare</h3>
      <p class="fb-brod">Idébolig er en boligbygger med base på Hamar. Vi
        kombinerer tidløs design med praktiske planløsninger, og legger vekt
        på at hjemmene vi bygger skal være både vakre å se på og gode å leve
        i — år etter år.</p>
      <p class="fb-brod">Bak hver modell ligger et grundig arbeid med
        arkitektur, arealbruk og materialvalg. Og fordi ingen tomter og ingen
        familier er like, tilpasser vi gjerne: flytt en vegg, legg til en
        garasje, eller la oss tegne noe helt eget for deg.</p>
      <p class="fb-brod">Vi bistår hele veien — fra byggteknisk rådgivning og
        byggesøknad til prosjektering, grunnarbeid og montasje. Det gir deg
        én partner å forholde deg til, og full oversikt fra første strek til
        ferdig bolig.</p>
      <span class="fb-sidenr fb-sidenr--h fb-sidenr--vs">{nr}</span>
    </div>"""


def sitatfotoside(nr: int) -> str:
    src = beste_bilde("wp-content/uploads/2024/11/Fasade-Nora")
    return (f'<div class="fb-foto"><img src="{src}" alt="Nora — fasade">'
            f'<p class="fb-sitat">«Hjemmene vi bygger skal være like gode å '
            f'leve i som de er å se på.»</p>'
            f'<span class="fb-sidenr fb-sidenr--v">{nr}</span></div>')


def oversiktside(boliger: list, nr: int, forste: bool) -> str:
    kort = []
    for b in boliger:
        bra = f'{b["bra"]} m²' + (" pr enhet" if b["braenhet"] else "")
        kort.append(f"""<div class="fb-kort">
          <img src="{beste_bilde(b['bilde'])}" alt="{b['navn']}">
          <b>{b['navn']}</b>
          <span class="fb-ki">{IKON['bra']}{bra}</span>
          <span class="fb-ki">{IKON['sov']}{b['sov']} soverom</span>
          <span class="fb-ki">{IKON['bad']}{b['bad']} bad</span>
        </div>""")
    topp = ("""<p class="fb-kicker">Boligmodellene</p>
      <h3>Utforsk våre boliger</h3>""" if forste else
            '<p class="fb-kicker">Boligmodellene</p><h3>&nbsp;</h3>')
    return f"""<div class="fb-info">
      {topp}
      <div class="fb-kortgrid">{''.join(kort)}</div>
      <span class="fb-sidenr {'fb-sidenr--h fb-sidenr--vs' if forste else 'fb-sidenr--h'}">{nr}</span>
    </div>"""


def prosesside(steg: list, start_nr: int, nr: int, forste: bool) -> str:
    rader = "".join(
        f'<li><b>{i}. {t}</b><p>{tekst}</p></li>'
        for i, (t, tekst) in enumerate(steg, start=start_nr))
    topp = ("""<p class="fb-kicker">Byggeprosessen</p>
      <h3>Fra idé til innflytting</h3>
      <p class="fb-brod fb-brod--liten">Slik jobber vi — steg for steg, med
        faste holdepunkter og én partner hele veien.</p>""" if forste else
            '<p class="fb-kicker">Byggeprosessen</p><h3>&nbsp;</h3>')
    return f"""<div class="fb-info">
      {topp}
      <ol class="fb-steg">{rader}</ol>
      <span class="fb-sidenr {'fb-sidenr--h fb-sidenr--vs' if forste else 'fb-sidenr--h'}">{nr}</span>
    </div>"""


def guideside(punkter: list, nr: int, forste: bool) -> str:
    rader = "".join(f'<li><b>{t}</b><p>{tekst}</p></li>' for t, tekst in punkter)
    topp = ("""<p class="fb-kicker">Guide</p>
      <h3>Slik velger du riktig boligmodell</h3>
      <p class="fb-brod fb-brod--liten">Seks ting det lønner seg å tenke
        gjennom før du bestemmer deg.</p>""" if forste else
            """<p class="fb-kicker">Guide</p><h3>&nbsp;</h3>""")
    bunn = ("" if forste else
            '<p class="fb-brod fb-brod--liten">Usikker? Vi hjelper deg å veie '
            'alternativene mot hverandre — helt uforpliktende.</p>')
    return f"""<div class="fb-info">
      {topp}
      <ol class="fb-steg fb-steg--guide">{rader}</ol>
      {bunn}
      <span class="fb-sidenr {'fb-sidenr--h fb-sidenr--vs' if forste else 'fb-sidenr--h'}">{nr}</span>
    </div>"""


def kontaktside(nr: int) -> str:
    return f"""<div class="fb-info">
      <p class="fb-kicker">Kontakt</p>
      <h3>Klar for neste steg?</h3>
      <p class="fb-brod">Ta kontakt for en uforpliktende prat om tomten din,
        boligmodellene eller prisoverslag. Vi svarer gjerne — og du binder
        deg ikke til noe.</p>
      <div class="fb-kontaktinfo">
        <p><b>Idébolig AS</b></p>
        <p>Jølstadbakken 14, 2318 Hamar</p>
        <p>91 92 66 66</p>
        <p>post@idebolig.no</p>
      </div>
      <a class="fb-lenke" href="../kontakt/">Send oss en melding →</a>
      <span class="fb-sidenr fb-sidenr--h fb-sidenr--vs">{nr}</span>
    </div>"""


def qrside(nr: int) -> str:
    return f"""<div class="fb-info fb-info--midt">
      <p class="fb-kicker">idebolig.no</p>
      <h3>Se mer på nettsiden</h3>
      <p class="fb-brod fb-brod--liten">Skann koden for flere bilder, alle
        boligmodellene og guidene våre.</p>
      {qr_svg()}
      <p class="fb-qrurl">idebolig.no</p>
      <span class="fb-sidenr fb-sidenr--h">{nr}</span>
    </div>"""


def tocside(seksjoner: list, modeller: list, nr: int) -> str:
    sek = "".join(
        f'<li class="fb-toc-sek"><b>{n} — {navn}</b>'
        f'<span class="prikker"></span><span class="nr">{side}</span></li>'
        for n, navn, side in seksjoner)
    mod = "".join(
        f'<li class="fb-toc-mod"><small>{navn}</small>'
        f'<span class="prikker"></span><span class="nr">{side}</span></li>'
        for navn, side in modeller)
    return f"""<div class="fb-info">
      <p class="fb-kicker">Katalog 2026</p>
      <h3>Innhold</h3>
      <ul class="fb-toc">{sek[:len(sek)]}</ul>
      <ul class="fb-toc fb-toc--modeller">{mod}</ul>
      <span class="fb-sidenr fb-sidenr--h">{nr}</span>
    </div>"""


def tjenesteside(nr: int) -> str:
    tj = ["Byggteknisk rådgivning", "Byggesøknad", "Arkitekttjenester",
          "Prosjektering", "Utførelse og montasje",
          "Graving, grunnarbeid og betongfundamentering"]
    li = "".join(f"<li>{t}</li>" for t in tj)
    return f"""<div class="fb-info">
      <p class="fb-kicker">Tjenester</p>
      <h3>Mer enn boligmodeller</h3>
      <p class="fb-brod">Vi bistår gjennom hele byggeprosessen:</p>
      <ul class="fb-tjenester">{li}</ul>
      <a class="fb-lenke" href="../tjenester/">Les mer om tjenestene →</a>
      <span class="fb-sidenr fb-sidenr--h fb-sidenr--vs">{nr}</span>
    </div>"""


def tilpasningside(nr: int) -> str:
    """Frisiden (s. 45): modellene som utgangspunkt, ikke fasit."""
    rader = "".join(f'<li><b>{t}</b><p>{tekst}</p></li>' for t, tekst in TILPASNING)
    return f"""<div class="fb-info">
      <p class="fb-kicker">Tilpasning</p>
      <h3>Modellene er et utgangspunkt</h3>
      <p class="fb-brod fb-brod--liten">Ingen tomt og ingen familie er lik.
        Dette er det som oftest justeres.</p>
      <ol class="fb-steg fb-steg--guide">{rader}</ol>
      <p class="fb-brod fb-brod--liten">Finner dere ikke modellen dere ser
        etter, tegner vi en helt egen — arkitekttjenester, prosjektering og
        byggesøknad er en del av det vi leverer.</p>
      <a class="fb-lenke" href="../kontakt/">Snakk med oss om tilpasning →</a>
      <span class="fb-sidenr fb-sidenr--h">{nr}</span>
    </div>"""


def bygg() -> None:
    forside = """<div class="fb-perm">
      <img src="../wp-content/uploads/2024/11/Hvit-logo-sidestilt.png" alt="Idébolig AS">
      <div class="fb-permlinje"></div>
      <h2>Boligkatalog</h2>
      <p class="fb-aar">2026</p>
      <p>Åtte boligmodeller — fra klassisk til funkis</p>
      <span class="fb-permhint">Dra i hjørnet, sveip eller bruk pilene for å bla</span>
    </div>"""
    bakside = """<div class="fb-perm fb-perm--bak">
      <img src="../wp-content/uploads/2024/11/Hvit-logo-sidestilt.png" alt="Idébolig AS">
      <div class="fb-permlinje"></div>
      <p>Idébolig AS · Jølstadbakken 14, 2318 Hamar</p>
      <p>91 92 66 66 · post@idebolig.no</p>
      <a class="fb-permlenke" href="../kontakt/">Ta kontakt →</a>
    </div>"""

    # Trykte sidetall: forsiden er unummerert, første innside er side 2, slik
    # at venstresider får partall som i en trykt katalog.
    BOLIG_START = 8
    base = BOLIG_START + 4 * len(BOLIGER)          # første side etter boligene
    seksjoner = [(1, "Velkommen", 2),
                 (2, "Om Idébolig", 4),
                 (3, "Boligmodellene", 6),
                 (4, "Byggeprosessen", base),
                 (5, "Slik velger du boligmodell", base + 2),
                 (6, "Tjenester, tilpasning og kontakt", base + 4)]
    modeller = [(b["navn"], BOLIG_START + 4 * n) for n, b in enumerate(BOLIGER)]

    innsider = [velkomstside(2), tocside(seksjoner, modeller, 3),
                omossside(4), sitatfotoside(5),
                oversiktside(BOLIGER[:4], 6, True),
                oversiktside(BOLIGER[4:], 7, False)]
    nr = BOLIG_START
    for b in BOLIGER:
        innsider += [fotoside(b["bilde"], b["navn"], nr), infoside(b, nr + 1)]
        if len(PLANER.get(b["slug"], [])) > 2:
            innsider += list(plansider(b, nr + 2, nr + 3))
        else:
            innsider += [duoside(MEDIA[b["slug"]], nr + 2), planside(b, nr + 3)]
        nr += 4
    innsider += [prosesside(PROSESS[:5], 1, nr, True),
                 prosesside(PROSESS[5:], 6, nr + 1, False),
                 guideside(GUIDE[:3], nr + 2, True),
                 guideside(GUIDE[3:], nr + 3, False),
                 tjenesteside(nr + 4), tilpasningside(nr + 5),
                 kontaktside(nr + 6), qrside(nr + 7)]

    # Bokas fysiske sider: hard perm + myke ark + hard perm. Innsider med
    # oddetallsindeks ligger til venstre i oppslaget → fals (ryggskygge) på
    # høyre kant; partallsindeks til høyre → fals på venstre kant.
    sider = ['<div class="side side--perm" data-density="hard">'
             f'{forside}</div>']
    for i, innhold in enumerate(innsider, start=1):
        fals = "fals--v" if i % 2 == 0 else "fals--h"
        sider.append(f'<div class="side">{innhold}'
                     f'<div class="fals {fals}"></div></div>')
    sider.append('<div class="side side--perm" data-density="hard">'
                 f'{bakside}</div>')
    sider_html = "\n".join(sider)
    antall = len(sider)
    oppslag = (antall - 2) // 2

    main = f"""
<style>
#fbk{{--gull:#C99C55;--mork:#33302C;--grå:#6b6257;--krem:#F7F3EC;--papir:#FDFBF7;
  font-family:Poppins,sans-serif;color:var(--mork);background:var(--krem);
  padding:80px 20px 100px}}
:where(#fbk *){{box-sizing:border-box;margin:0}}
.fbk-indre{{max-width:1160px;margin:0 auto}}
.fbk-topp{{max-width:640px;margin:0 auto 44px;text-align:center}}
.fbk-kicker{{display:flex;align-items:center;justify-content:center;gap:14px;
  font:600 12px/1 Inter,sans-serif;letter-spacing:.24em;text-transform:uppercase;
  color:var(--gull);margin-bottom:20px}}
.fbk-kicker::before,.fbk-kicker::after{{content:"";flex:0 0 46px;height:1px;
  background:var(--gull);opacity:.55}}
#fbk h1{{font-size:clamp(32px,4.5vw,48px);font-weight:700;letter-spacing:-.015em;
  margin-bottom:16px}}
.fbk-intro{{color:var(--grå);font-size:15.5px;line-height:1.7}}
.fbk-scene{{max-width:1020px;margin:0 auto;filter:drop-shadow(0 24px 44px rgba(51,48,44,.28))}}
.side{{background:var(--papir);overflow:hidden;border:1px solid rgba(51,48,44,.06)}}
.side--perm{{border:0}}
.fals{{position:absolute;top:0;bottom:0;width:5.5%;pointer-events:none;z-index:3}}
.fals--h{{right:0;background:linear-gradient(to left,rgba(0,0,0,.10),transparent)}}
.fals--v{{left:0;background:linear-gradient(to right,rgba(0,0,0,.10),transparent)}}
.fb-sidenr{{position:absolute;bottom:11px;margin:0!important;
  font:600 11px Inter,sans-serif;letter-spacing:.06em;z-index:2}}
.fb-sidenr--v{{left:16px;color:rgba(255,255,255,.85)}}
.fb-sidenr--h{{right:16px;color:var(--grå)}}
.fb-sidenr--vs{{right:auto;left:16px;color:var(--grå)}}
.fb-foto{{position:absolute;inset:0}}
.fb-foto img{{width:100%;height:100%;object-fit:cover}}
.fb-foto p{{position:absolute;left:0;right:0;bottom:0;margin:0!important;
  padding:34px 28px 16px;color:#fff;font:700 24px Poppins,sans-serif;
  background:linear-gradient(to top,rgba(24,22,19,.78),rgba(24,22,19,.25) 70%,transparent)}}
.fb-duo{{position:absolute;inset:0;display:flex;flex-direction:column;gap:3px}}
.fb-duo figure{{position:relative;flex:1;overflow:hidden}}
.fb-duo img{{width:100%;height:100%;object-fit:cover;display:block}}
.fb-duo figcaption{{position:absolute;left:0;right:0;bottom:0;
  padding:24px 16px 10px;color:#fff;font:600 11px Inter,sans-serif;
  letter-spacing:.1em;text-transform:uppercase;
  background:linear-gradient(to top,rgba(24,22,19,.6),transparent)}}
.fb-info{{position:absolute;inset:0;padding:8% 9%;display:flex;flex-direction:column}}
.fb-kicker{{font:600 10.5px Inter,sans-serif;letter-spacing:.2em;text-transform:uppercase;
  color:var(--gull);margin-bottom:10px}}
.fb-info h3{{font-size:clamp(20px,2.6vw,30px);font-weight:700;margin-bottom:6px}}
.fb-tagline{{color:var(--grå);font-size:clamp(11px,1.3vw,14px);line-height:1.55;margin-bottom:14px}}
.fb-specs{{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:14px}}
.fb-spec{{background:var(--krem);border-radius:8px;padding:8px 11px}}
.fb-spec span{{display:block;font:600 9px Inter,sans-serif;letter-spacing:.12em;
  text-transform:uppercase;color:var(--gull)}}
.fb-spec b{{font-size:clamp(11px,1.4vw,14.5px)}}
.fb-tekst{{color:var(--grå);font-size:clamp(10.5px,1.25vw,13.5px);line-height:1.65;flex:1;overflow:hidden}}
.fb-tekst--kort{{flex:0 1 auto;margin-top:12px}}
.fb-brod{{color:var(--grå);font-size:clamp(11px,1.35vw,14px);line-height:1.7;margin-bottom:12px}}
.fb-sign{{margin-top:auto;font:600 clamp(11px,1.3vw,13.5px) Poppins,sans-serif;color:var(--gull)}}
.fb-lenke{{font:600 clamp(11px,1.3vw,14px) Poppins,sans-serif;color:var(--gull);text-decoration:none}}
.fb-toc{{list-style:none;padding:0;flex:1;display:flex;flex-direction:column;
  justify-content:center;gap:0;margin-top:6px}}
.fb-toc li{{display:flex;align-items:baseline;gap:9px;padding:2% 0;
  border-bottom:1px solid rgba(107,98,87,.14);font-size:clamp(11px,1.45vw,15px)}}
.fb-toc li:last-child{{border-bottom:0}}
.fb-toc b{{font-weight:600}}
.fb-toc small{{color:var(--grå);font:500 clamp(8px,1vw,10px) Inter,sans-serif;
  letter-spacing:.07em;text-transform:uppercase}}
.fb-toc .prikker{{flex:1;border-bottom:1px dotted rgba(107,98,87,.45);
  transform:translateY(-3px)}}
.fb-toc .nr{{font:600 clamp(10px,1.25vw,12.5px) Inter,sans-serif;color:var(--gull)}}
.fb-tjenester{{list-style:none;padding:0;margin:2px 0 14px;flex:1;display:flex;
  flex-direction:column;justify-content:center;gap:0}}
.fb-tjenester li{{position:relative;padding:1.8% 0 1.8% 20px;
  border-bottom:1px solid rgba(107,98,87,.14);
  font-size:clamp(11px,1.35vw,14.5px)}}
.fb-tjenester li:last-child{{border-bottom:0}}
.fb-tjenester li::before{{content:"";position:absolute;left:2px;top:50%;
  width:7px;height:7px;border-radius:50%;background:var(--gull);translate:0 -50%}}
.fb-ph{{flex:1;min-height:0;border:2px dashed rgba(201,156,85,.55);border-radius:12px;
  background:var(--krem);display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:9px;text-align:center;padding:6% 8%;margin:8px 0}}
.fb-ph-chip{{font:700 9.5px Inter,sans-serif;letter-spacing:.18em;
  text-transform:uppercase;color:#fff;background:var(--gull);
  padding:6px 12px;border-radius:99px}}
.fb-ph b{{font:600 clamp(12.5px,1.6vw,17px) Poppins,sans-serif}}
.fb-ph p{{color:var(--grå);font-size:clamp(10px,1.2vw,12.5px);line-height:1.55}}
.fb-planer{{flex:1;min-height:0;display:flex;flex-direction:column;gap:6px;margin:8px 0}}
.fb-planfig{{position:relative;flex:1;min-height:0;background:var(--krem);
  border-radius:10px;overflow:hidden}}
.fb-planfig img{{width:100%;height:100%;object-fit:contain;display:block}}
.fb-planfig figcaption{{position:absolute;left:8px;bottom:8px;
  font:600 9.5px Inter,sans-serif;letter-spacing:.09em;text-transform:uppercase;
  color:var(--mork);background:rgba(253,251,247,.85);
  padding:4px 9px;border-radius:99px}}
.fb-hl{{list-style:none;padding:0;margin:0 0 10px}}
.fb-hl li{{position:relative;padding:1.1% 0 1.1% 20px;
  font:500 clamp(10.5px,1.25vw,13.5px) Poppins,sans-serif}}
.fb-hl li::before{{content:"";position:absolute;left:2px;top:50%;width:7px;height:7px;
  border-radius:50%;background:var(--gull);translate:0 -50%}}
.fb-kortgrid{{flex:1;min-height:0;display:grid;grid-template-columns:1fr 1fr;
  grid-template-rows:1fr 1fr;gap:4% 6%;margin-top:8px}}
.fb-kort{{display:flex;flex-direction:column;min-height:0}}
.fb-kort img{{width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:8px;
  margin-bottom:6px;min-height:0}}
.fb-kort b{{font-size:clamp(11px,1.5vw,15px);margin-bottom:3px}}
.fb-ki{{display:flex;align-items:center;gap:6px;
  font:500 clamp(8.5px,1.05vw,11px) Inter,sans-serif;color:var(--grå);
  padding:1px 0}}
.fb-ki svg{{width:1.1em;height:1.1em;color:var(--gull);flex:0 0 auto}}
.fb-steg{{list-style:none;padding:0;margin:6px 0 0;flex:1;display:flex;
  flex-direction:column;justify-content:space-evenly}}
.fb-steg li b{{display:block;font-size:clamp(10.5px,1.3vw,13.5px);
  color:var(--mork);margin-bottom:1px}}
.fb-steg li p{{color:var(--grå);font-size:clamp(9.5px,1.12vw,12px);line-height:1.5}}
.fb-steg--guide li b{{color:var(--gull)}}
.fb-brod--liten{{font-size:clamp(10px,1.2vw,12.5px);margin-bottom:6px}}
.fb-kontaktinfo{{background:var(--krem);border-radius:12px;padding:6% 8%;
  margin:4% 0;flex:0 0 auto}}
.fb-kontaktinfo p{{font-size:clamp(11px,1.35vw,14.5px);line-height:1.8;color:var(--mork)}}
.fb-info--midt{{align-items:center;text-align:center}}
.fb-qr{{width:52%;height:auto;max-width:300px;margin:5% 0 3%;
  border-radius:10px;box-shadow:0 4px 18px rgba(51,48,44,.14)}}
.fb-qrurl{{font:600 clamp(12px,1.5vw,16px) Poppins,sans-serif;color:var(--gull)}}
.fb-sitat{{font-size:clamp(14px,1.9vw,22px)!important;font-weight:600!important;
  line-height:1.45!important;padding:44px 9% 22px!important}}
.fb-toc-sek b{{font-size:clamp(10.5px,1.3vw,13.5px);letter-spacing:.02em}}
.fb-toc--modeller{{flex:0 1 auto;margin-top:2px}}
.fb-toc--modeller li{{padding:1.1% 0 1.1% 16px}}
.fb-toc--modeller small{{font:500 clamp(9px,1.1vw,11.5px) Inter,sans-serif;
  letter-spacing:.05em;text-transform:none;color:var(--mork)}}
.fb-perm{{position:absolute;inset:0;background:linear-gradient(150deg,#3A362F,#26231F);
  color:#D9D2C5;display:flex;flex-direction:column;align-items:center;
  justify-content:center;text-align:center;padding:10%}}
.fb-perm img{{width:46%;max-width:230px;margin-bottom:22px}}
.fb-permlinje{{width:52px;height:2px;background:var(--gull);margin-bottom:22px}}
.fb-perm h2{{font-size:clamp(24px,3.4vw,38px);font-weight:700;color:#fff;
  letter-spacing:.04em;margin-bottom:4px}}
.fb-aar{{font:600 clamp(15px,2vw,22px) Poppins,sans-serif;color:var(--gull);
  letter-spacing:.28em;margin-bottom:12px!important}}
.fb-perm p{{font-size:clamp(11px,1.4vw,15px);line-height:1.7}}
.fb-permhint{{margin-top:26px;font:500 clamp(10px,1.2vw,12.5px) Inter,sans-serif;opacity:.65}}
.fb-permlenke{{margin-top:18px;font:600 clamp(12px,1.4vw,15px) Poppins,sans-serif;
  color:var(--gull);text-decoration:none}}
.fbk-kontroll{{display:flex;align-items:center;justify-content:center;gap:20px;margin-top:38px}}
.fbk-kontroll button{{flex:0 0 46px;width:46px;height:46px;border-radius:50%;
  border:1.5px solid #E3DCCF;background:#fff;color:var(--mork);font-size:19px;
  cursor:pointer;transition:.2s;padding:0;line-height:1;min-width:0}}
.fbk-kontroll button:hover:not([disabled]){{background:var(--gull);border-color:var(--gull);color:#fff}}
.fbk-kontroll button[disabled]{{opacity:.35;cursor:default}}
.fbk-teller{{font:500 13.5px Inter,sans-serif;color:var(--grå);min-width:110px;text-align:center}}
#fbk-full{{font-size:15px}}
#fbk:fullscreen{{display:flex;flex-direction:column;justify-content:center;
  overflow:auto;padding:24px 20px}}
#fbk:fullscreen .fbk-topp{{display:none}}
#fbk:fullscreen .fbk-scene{{max-width:min(1500px,94vw)}}
@media(max-width:700px){{
 #fbk{{padding:56px 12px 70px}}
 .fbk-topp{{padding:0 16px}}
 .fb-foto p{{font-size:19px}}
 .fb-info{{padding:7% 8%}}
 .fb-specs{{gap:5px}}
}}
</style>
<section id="fbk">
 <div class="fbk-indre">
  <div class="fbk-topp">
    <p class="fbk-kicker">Bla i katalogen</p>
    <h1>Boligkatalog 2026</h1>
    <p class="fbk-intro">Bla deg gjennom boligene våre som i en ekte katalog —
      ta tak i hjørnet og dra, sveip, eller bruk pilene.</p>
  </div>
  <div class="fbk-scene">
    <div id="fbk-bok">
{sider_html}
    </div>
  </div>
  <div class="fbk-kontroll">
    <button id="fb-forrige" aria-label="Forrige side">‹</button>
    <span class="fbk-teller" id="fb-teller"></span>
    <button id="fb-neste" aria-label="Neste side">›</button>
    <button id="fbk-full" aria-label="Fullskjerm" title="Fullskjerm">⛶</button>
  </div>
 </div>
</section>
<script src="page-flip.browser.js"></script>
<script>
(function(){{
 var ANTALL={antall},OPPSLAG={oppslag};
 var teller=document.getElementById('fb-teller'),
     knappF=document.getElementById('fb-forrige'),
     knappN=document.getElementById('fb-neste'),
     full=document.getElementById('fbk-full'),
     seksjon=document.getElementById('fbk');
 var bok=new St.PageFlip(document.getElementById('fbk-bok'),{{
  width:510,height:680,size:'stretch',
  minWidth:290,maxWidth:760,minHeight:387,maxHeight:1013,
  showCover:true,usePortrait:true,
  maxShadowOpacity:.45,flippingTime:850,swipeDistance:24,
  showPageCorners:true,mobileScrollSupport:false
 }});
 bok.loadFromHTML(document.querySelectorAll('#fbk-bok .side'));
 function oppdater(){{
  var i=bok.getCurrentPageIndex(),staaende=bok.getOrientation()==='portrait';
  if(i<=0)teller.textContent='Forside';
  else if(i>=ANTALL-1)teller.textContent='Bakside';
  else if(staaende)teller.textContent='Side '+i+' av '+(ANTALL-2);
  else teller.textContent='Oppslag '+Math.ceil(i/2)+' av '+OPPSLAG;
  knappF.disabled=i<=0;
  knappN.disabled=i>=ANTALL-1;
 }}
 bok.on('flip',oppdater);
 bok.on('changeOrientation',oppdater);
 knappN.addEventListener('click',function(){{bok.flipNext();}});
 knappF.addEventListener('click',function(){{bok.flipPrev();}});
 document.addEventListener('keydown',function(e){{
  if(e.key==='ArrowRight'||e.key==='Right')bok.flipNext();
  if(e.key==='ArrowLeft'||e.key==='Left')bok.flipPrev();}});
 if(seksjon.requestFullscreen){{
  full.addEventListener('click',function(){{
   if(document.fullscreenElement)document.exitFullscreen();
   else seksjon.requestFullscreen();
  }});
 }}else{{full.style.display='none';}}
 oppdater();
}})();
</script>
"""

    skall = (ROOT / "våre-boliger" / "index.html").read_text(encoding="utf-8")
    start = re.search(r"<main[^>]*>", skall)
    end = skall.find("</main>")
    side = skall[: start.end()] + main + skall[end:]
    side = side.replace(
        "<title>Boligkatalog &#8211; Idébolig AS</title>",
        "<title>Boligkatalog 2026 &#8211; Idébolig AS</title>\n"
        '<meta name="robots" content="noindex, nofollow" />')
    side = side.replace(
        'href="https://idebolig.no/v%C3%A5re-boliger/"',
        f'href="https://idebolig.no/{SLUG}/"')
    (ROOT / SLUG).mkdir(exist_ok=True)
    (ROOT / SLUG).joinpath("index.html").write_text(side, encoding="utf-8")
    if not (ROOT / SLUG / "page-flip.browser.js").exists():
        raise SystemExit("MANGLER: page-flip.browser.js må ligge i katalogmappa")
    print(f"Skrev katalog med {antall} sider ({oppslag} oppslag) til {SLUG}/index.html")


if __name__ == "__main__":
    bygg()
