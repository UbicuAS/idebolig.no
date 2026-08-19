# -*- coding: utf-8 -*-
"""
Rydder sidehodet etter WordPress og retter canonical-lenkene.

Speilingen fra WordPress tok med seg hodemarkering som ikke lenger stemmer nå
som siden er statisk. Skriptet gjør fire ting, alle idempotente:

  1. CANONICAL blir absolutt mot https://idebolig.no.
     Speileren gjorde de absolutte canonical-lenkene relative, og en relativ
     canonical er verre enn ingen: på forsiden pekte den på `index.html`, altså
     https://idebolig.no/index.html — en annen URL enn https://idebolig.no/, så
     forsiden konkurrerte med seg selv. På forhåndsvisningen
     (idebolig.ubicu.cloud, samme filer) pekte hver side på seg selv i stedet
     for på produksjonssiden, så hele siden lå ute som duplikat.

     Samtidig brytes en canonical-løkke: /edvard/ pekte på /edvard.html mens
     /edvard.html pekte på /edvard/. Sitemapet regner /edvard/ som den
     kanoniske, så det er den som gjelder — begge peker nå dit.

  2. SPRÅK settes til nb-NO. Sidene sto som en-US fra WordPress-oppsettet,
     på et innhold som er norsk hele veien.

  3. DØDE LENKER i hodet fjernes: RSS-feed, kommentar-feed, oEmbed (JSON og
     XML), wp-json-API-et, side-JSON, RSD/xmlrpc og shortlink. Alle sju
     endepunktene svarer 404 nå som WordPress er arkivert.

  4. GENERATOR-META for WordPress og Site Kit fjernes. Den er feil (siden
     kjører ikke WordPress) og den er et skilt til alle skannere som leter
     etter wp-login. Elementors generator-meta beholdes — den CSS-en og
     JS-en ligger der faktisk.

Kjøres fra rotmappen:  python tools/rydd_wp_hoder.py
"""
import io
import re
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
BASIS = "https://idebolig.no"

# fil -> kanonisk URL-sti. Æ/Ø/Å prosentkodes, slik de gjør i sitemapet.
KANONISK = {
    "index.html":                 "/",
    "about/index.html":           "/about/",
    "alva/index.html":            "/alva/",
    "boligkatalog/index.html":    "/boligkatalog/",
    "edvard/index.html":          "/edvard/",
    "edvard-prakt/index.html":    "/edvard-prakt/",
    "embla/index.html":           "/embla/",
    "kontakt/index.html":         "/kontakt/",
    "nora/index.html":            "/nora/",
    "odin/index.html":            "/odin/",
    "prosjekter/index.html":      "/prosjekter/",
    "tiril/index.html":           "/tiril/",
    "til-salgs/index.html":       "/til-salgs/",
    "tjenester/index.html":       "/tjenester/",
    "vilde/index.html":           "/vilde/",
    "våre-boliger/index.html":    "/v%C3%A5re-boliger/",
    # Duplikater som med vilje peker et annet sted enn seg selv:
    "boligkatalog-ny/index.html": "/v%C3%A5re-boliger/",   # samme side som våre-boliger
    "edvard.html":                "/edvard/",              # gammel enkeltfil-URL
}

# Hodelenker som peker på WordPress-endepunkter som ikke finnes lenger.
DODE = [
    re.compile(r'^<link rel="alternate" type="application/rss\+xml".*?/>\s*\n', re.M),
    re.compile(r'^<link rel="alternate" title="oEmbed \((?:JSON|XML)\)".*?/>\s*\n', re.M),
    re.compile(r'^<link rel="https://api\.w\.org/".*?/>\s*\n', re.M),
    re.compile(r'^<link rel="alternate" title="JSON" type="application/json".*?/>\s*\n', re.M),
    re.compile(r'^<link rel="EditURI".*?/>\s*\n', re.M),
    re.compile(r"^<link rel='shortlink'.*?/>\s*\n", re.M),
    # Generator-metaene ligger ikke alltid alene på en linje — Site Kit og
    # Elementor deler linje på flere sider — så disse to matches på tag-nivå.
    re.compile(r'<meta name="generator" content="WordPress[^"]*"\s*/>\n?'),
    re.compile(r'<meta name="generator" content="Site Kit by Google[^"]*"\s*/>\n?'),
]

CANONICAL = re.compile(r'(<link rel=["\']canonical["\'][^>]*href=["\'])([^"\']+)(["\'])')
SPRAK = re.compile(r'(<html[^>]*\blang=["\'])([^"\']+)(["\'])')

endret = 0
for rel, sti in sorted(KANONISK.items()):
    fil = ROT / rel
    if not fil.exists():
        print("FANT IKKE  " + rel)
        continue

    # Filene er sjekket ut med CRLF (core.autocrlf=true). Leses de i tekstmodus
    # og skrives tilbake, blir de LF — som gir riktig git-diff, men bytter
    # linjeslutt på hver eneste linje i fila som lastes opp til serveren.
    # Derfor: les binært, arbeid med LF, skriv tilbake med opprinnelig slutt.
    rådata = fil.read_bytes()
    crlf = b"\r\n" in rådata
    tekst = rådata.decode("utf-8").replace("\r\n", "\n")
    for_ = tekst
    notat = []

    ny_canonical = BASIS + sti
    if CANONICAL.search(tekst):
        gammel = CANONICAL.search(tekst).group(2)
        if gammel != ny_canonical:
            tekst = CANONICAL.sub(lambda m: m.group(1) + ny_canonical + m.group(3), tekst, count=1)
            notat.append("canonical %s -> %s" % (gammel, ny_canonical))
    else:
        notat.append("MANGLER canonical")

    m = SPRAK.search(tekst)
    if m and m.group(2) != "nb-NO":
        tekst = SPRAK.sub(lambda mm: mm.group(1) + "nb-NO" + mm.group(3), tekst, count=1)
        notat.append("lang %s -> nb-NO" % m.group(2))

    fjernet = 0
    for m0nster in DODE:
        tekst, n = m0nster.subn("", tekst)
        fjernet += n
    if fjernet:
        notat.append("fjernet %d døde hodelenker" % fjernet)

    if tekst != for_:
        ut = tekst.replace("\n", "\r\n") if crlf else tekst
        fil.write_bytes(ut.encode("utf-8"))
        endret += 1
        print("%-28s %s" % (rel, "; ".join(notat)))
    else:
        print("%-28s uendret" % rel)

print("\n%d av %d filer endret" % (endret, len(KANONISK)))
