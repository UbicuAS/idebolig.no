# -*- coding: utf-8 -*-
"""Møblerte 2D-plantegninger for Alva — VERSJON 2 (korrigert 21.08.2026 etter
Marius' tilbakemelding om uterommene).

Fasit fra fasadebildene (Fasade-Alva-hero + Fasade-3) og CAD-skjermbildene:
- FRONT: terrasse 16,9 m² i TO felt langs hele fasaden, delt av inngangstrappa
  i midten; hoveddør midt på; skyvedører fra stue og kjøkken.
- Balkong 11 m² i FULL BREDDE over terrassen (på søyler), dør fra loftstua.
- BAK: egen inngangsdør m/ skjermtak inn til gangen.
- Soverommet i 1. etg ligger i et UTBYGG bak; balkong 9,9 m² ligger oppå
  utbyggets tak, og 2. etg har tilsvarende utsparing i fotavtrykket.
- Stue + kjøkken vender mot fronten; boder/trapp/gang/bad ligger bak.
Front tegnes øverst (nord i tegningen)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from alva_helpers import (MAPPE, MORK, GRAA, GULL, PARKETT, PARKETT_L, FLIS,
                          FLIS_L, DEKKE, DEKKE_L, BETONG, BETONG_L, MOEBEL,
                          MOEBEL_K, YV, IV, r, linje, tekst, romnavn, sone,
                          vindu, door, mobel_rect, seng, nattbord, garderobe,
                          sofa, bord, stol, vask, komfyr, toalett, dusj,
                          badekar, vaskemaskin, teppe, trapp, hylle, HODE)
import alva_helpers

B = 11200   # bredde
D = 9800    # dybde
UTB_X = 6900   # utbygg/balkong 9,9: x 6900..11200, y 7900..9800 (bak, øst)


def skriv(navn, viewbox, tittel):
    tx, ty = tittel
    tekst(tx, ty, f"Alva — {navn}", 380, MORK, 600, anker="start")
    fil = Path(MAPPE) / f"alva-{navn.replace('. ', '').replace(' ', '-').lower()}.svg"
    svg = HODE.replace("{VB}", viewbox) + "\n".join(alva_helpers.deler) + "\n</svg>\n"
    fil.write_text(svg, encoding="utf-8")
    print("skrev", fil, len(svg))
    alva_helpers.deler.clear()


def rekkverk(x1, y, x2, tykk=70):
    """Rekkverkslinje (dobbel strek) langs en horisontal kant."""
    linje(x1, y, x2, y, MORK, 40)
    linje(x1, y + tykk, x2, y + tykk, GRAA, 22)


def skyvedor(x, y, lengde):
    """Skyvedør i horisontal yttervegg."""
    r(x, y, lengde, YV, "url(#parkett)")
    linje(x, y + YV / 2, x + lengde, y + YV / 2, MORK, 30)
    linje(x, y + 30, x + lengde, y + 30, MORK, 22)


# ================================================================ 1. ETASJE
def etg1():
    alva_helpers.deler.append(
        f'<path d="M 0 0 H {B} V {D} H 0 Z" fill="#FDFBF7" filter="url(#skygge)"/>')
    # TERRASSE foran i to felt + inngangstrapp i midten (fasadefasit)
    r(0, -1800, 4900, 1800, "url(#dekke)")
    r(6300, -1800, B - 6300, 1800, "url(#dekke)")
    rekkverk(0, -1870, 4900); rekkverk(6300, -1870, B)
    linje(0, -1800, 0, 0, MORK, 40); linje(B, -1800, B, 0, MORK, 40)
    trapp(4900, -1800, 1400, 1750, opp="n", trinn=5, tekst_under=False)
    # inngangsrepos bak (to trinn + skjermtak)
    r(4950, D, 1300, 900, "url(#dekke)")
    linje(4950, D + 300, 6250, D + 300, DEKKE_L, 24)
    linje(4700, D + 60, 6500, D + 60, GRAA, 30, dash="160 90")   # skjermtak
    # gulv
    r(0, 0, B, D, "url(#parkett)")
    r(6300, 4300, 2600, 2600, "url(#flis)")                 # bad
    # yttervegger
    r(0, 0, B, YV, MORK)
    r(0, 0, YV, D, MORK)
    r(0, D - YV, B, YV, MORK)
    r(B - YV, 0, YV, D, MORK)
    # innervegger
    r(0, 6800 - IV, 3000, IV, MORK)                         # stueflik | bod/tek
    r(3000, 4600, IV, 5200, MORK)                           # vest | midt
    r(3000, 4600, 1700, IV, MORK)                           # stue | bod 2,6
    r(4700, 4600, IV, 5200, MORK)                           # bod/trapp | gang
    r(3000, 6300, 1700, IV, MORK)                           # bod 2,6 | trapp
    r(6300, 4300, IV, 5500, MORK)                           # gang | bad/sov
    r(6300, 4300, 4900, IV, MORK)                           # kjøkken | bad-sone
    r(8900, 4300, IV, 2600 + IV, MORK)                      # bad | gard-sone
    r(6300, 6900, 4900, IV, MORK)                           # bad/gard | soverom
    # skyvedører + hoveddør + vinduer
    skyvedor(1400, 0, 1800)                                 # stue -> terrasse
    skyvedor(8700, 0, 1600)                                 # kjøkken -> terrasse
    door(5150, 0, 900, YV, "h", "start", "inn")             # HOVEDINNGANG front midt
    vindu(0, 1200, 1600, "v")                               # stue vest
    vindu(0, 3600, 1300, "v")                               # stue vest 2
    vindu(0, 7600, 1200, "v")                               # bod/tek vest
    vindu(1000, D - YV, 1100, "h")                          # bod/tek sør
    vindu(B - YV, 1000, 1500, "v")                          # kjøkken øst
    vindu(7300, D - YV, 1300, "h")                          # soverom sør (utbygget)
    vindu(9500, D - YV, 1300, "h")                          # soverom sør 2
    vindu(B - YV, 5000, 900, "v")                           # gard-sone øst
    # dører innvendig
    door(5100, D - YV, 900, YV, "h", "start", "inn")                      # BAKINNGANG -> gang
    r(4700, 4600, 1600 + IV, IV, "url(#parkett)")                         # åpning stue -> gang
    door(4700, 5000, 800, IV, "v", "end", "ut", gulv=PARKETT)             # gang -> bod 2,6
    r(4700, 6500, IV, 1900, "url(#parkett)")                              # åpning gang -> trapp
    door(6300, 4900, 800, IV, "v", "start", "inn", gulv=FLIS)             # gang -> bad
    door(6300, 7300, 890, IV, "v", "start", "inn", gulv=PARKETT)          # gang -> soverom
    door(1700, 6800 - IV, 890, IV, "h", "end", "ut", gulv=PARKETT)        # stueflik -> bod/tek
    door(9500, 6900, 800, IV, "h", "start", "ut", gulv=PARKETT)           # sov -> gard-sone
    # trapp (innvendig)
    trapp(3100, 6400, 1500, 2200, opp="n", trinn=9, tekst_under=False)
    tekst(3850, 8950, "OPP", 170, GRAA, 500)
    # STUE — sofagruppe mot vestvinduene, tv mot sørfliken
    sofa(700, 2700, 2600, 950)
    bord(1500, 1600, 1100, 650, rx=200)
    teppe(900, 1400, 2500, 1000)
    hylle(1000, 4100, 1800, 420)
    mobel_rect(4200, 700, 450, 1500)                        # skjenk
    # KJØKKEN — benk langs øst + halvøy
    hylle(B - YV - 620, 1700, 620, 2400)
    komfyr(B - YV - 600, 2000, 500)
    vask(10650, 3600, 150)
    hylle(7000, 2900, 1900, 600)                            # halvøy
    bord(7300, 900, 1700, 900, rx=120)                      # spisebord
    stol(7450, 430); stol(8250, 430); stol(7450, 1870); stol(8250, 1870)
    # BOD 2,6 + BOD/TEK
    hylle(3100, 4750, 420, 1300)
    vaskemaskin(300, 7100); vaskemaskin(950, 7100)
    alva_helpers.deler.append(
        f'<circle cx="2350" cy="9100" r="330" fill="{MOEBEL}" '
        f'stroke="{MOEBEL_K}" stroke-width="20"/>')
    tekst(2350, 9170, "VV", 170, MOEBEL_K, 600)
    hylle(300, 8900, 1300, 420)
    # GANG
    teppe(5000, 8700, 1000, 700)
    # BAD
    dusj(6500, 4500, 850)
    vask(8300, 4750, 160)
    toalett(8350, 6100, "s")
    # SOVEROM (utbygget) + garderobenisje
    seng(7200, 7300, 1600, 2000)
    garderobe(9100, 4600, 550, 2100)
    garderobe(9800, 4600, 550, 2100)
    nattbord(9100, 7150)
    # romnavn
    romnavn(2250, 3000, "Stue", 41.8)
    romnavn(8700, 2400, "Kjøkken", 17.1)
    tekst(3850, 5600, "Bod", 200, MORK, 600); tekst(3850, 5840, "2,6 m²", 160, GRAA, 400)
    romnavn(1500, 8100, "Bod/Tek.", 7.2, s1=270, s2=210)
    romnavn(5500, 6300, "Gang", 8.2, s1=260, s2=200)
    romnavn(7500, 5900, "Bad", 6.9, s1=260, s2=200)
    romnavn(8600, 8300, "Soverom", 10, s1=260, s2=200)
    tekst(2400, -950, "Terrasse 16,9 m²", 250, GRAA, 600)
    tekst(9000, -950, "Terrasse", 250, GRAA, 600)
    tekst(5600, -2150, "Inngang", 200, GRAA, 500)
    tekst(5600, 11050, "Inngang bak", 200, GRAA, 500)
    sone(1500, -2400, "1. ETASJE")
    skriv("1. etasje", "-700 -3100 12800 14900", (-500, 11400))


# ================================================================ 2. ETASJE
# Kropp = 11200 x 9800 MINUS utsparing (x 6900..11200, y 7900..9800) der
# balkong 9,9 ligger på taket av soveromsutbygget.
def etg2():
    alva_helpers.deler.append(
        f'<path d="M 0 0 H {B} V 7900 H {UTB_X} V {D} H 0 Z" '
        'fill="#FDFBF7" filter="url(#skygge)"/>')
    # BALKONG 11 m² i full bredde over terrassen
    r(0, -1050, B, 1050, "url(#dekke)")
    rekkverk(0, -1120, B)
    linje(0, -1050, 0, 0, MORK, 40); linje(B, -1050, B, 0, MORK, 40)
    # BALKONG 9,9 m² på utbyggets tak (bak, øst)
    r(UTB_X, 7900, B - UTB_X + 400, 1900, "url(#dekke)")
    rekkverk(UTB_X, 9800, B + 400)
    linje(B + 400, 7900, B + 400, 9800, MORK, 40)
    # gulv
    alva_helpers.deler.append(
        f'<path d="M 0 0 H {B} V 7900 H {UTB_X} V {D} H 0 Z" fill="url(#parkett)"/>')
    r(8300, 3450, 2900, 1950, "url(#flis)")                 # bad 6,1
    r(4700, 5400, 2200, 2500, "url(#flis)")                 # wc/bad 6,7
    # yttervegger
    r(0, 0, B, YV, MORK)
    r(0, 0, YV, D, MORK)
    r(0, D - YV, UTB_X, YV, MORK)
    r(UTB_X - YV, 7900, YV, D - 7900, MORK)
    r(UTB_X, 7900 - YV, B - UTB_X, YV, MORK)                # mot balkong 9,9
    r(B - YV, 0, YV, 7900, MORK)
    # innervegger
    r(3700, 0, IV, 3450, MORK)                              # sov A | stue
    r(7400, 0, IV, 3450, MORK)                              # stue | sov B
    r(0, 3450, B, IV, MORK)                                 # topprad sør
    r(2100, 3450, IV, 1950, MORK)                           # bod | gang
    r(8300, 3450, IV, 1950, MORK)                           # gang | bad 6,1
    r(0, 5400, B, IV, MORK)                                 # midtbånd sør
    r(3000, 5400, IV, 4400, MORK)                           # sov C | trapp
    r(4700, 5400, IV, 2500, MORK)                           # trapp | wc/bad (åpent mot nisjen sør)
    r(6900, 5400, IV, 2500, MORK)                           # wc/bad | gardnisje
    r(8100, 5400, IV, 2500, MORK)                           # gardnisje | sov D
    r(4700, 7900, 2200, IV, MORK)                           # wc/bad sør (mot nisje)
    # vinduer
    vindu(1100, 0, 1400, "h")                               # sov A nord
    vindu(8300, 0, 1400, "h")                               # sov B nord
    vindu(0, 1200, 1300, "v")                               # sov A vest
    vindu(0, 6600, 1300, "v")                               # sov C vest
    vindu(1100, D - YV, 1500, "h")                          # sov C sør
    vindu(B - YV, 1200, 1300, "v")                          # sov B øst
    vindu(B - YV, 4200, 900, "v")                           # bad 6,1 øst
    vindu(B - YV, 6200, 1200, "v")                          # sov D øst
    # dører
    skyvedor(5300, 0, 1000)                                 # stue -> balkong 11
    door(8600, 7900 - YV, 900, YV, "h", "start", "ut", gulv=DEKKE)        # sov D -> balkong 9,9
    door(600, 3450, 890, IV, "h", "end", "ut", gulv=PARKETT)              # sov A
    door(4100, 3450, 890, IV, "h", "start", "ut", gulv=PARKETT)           # stue
    door(7600, 3450, 890, IV, "h", "start", "ut", gulv=PARKETT)           # sov B (fra gangen)
    door(2100, 4000, 800, IV, "v", "end", "ut", gulv=PARKETT)             # bod
    door(8300, 4200, 800, IV, "v", "start", "inn", gulv=FLIS)             # bad 6,1
    door(900, 5400, 890, IV, "h", "start", "inn", gulv=PARKETT)           # sov C
    r(3000, 5400, 1700 + IV, IV, "url(#parkett)")                         # åpning gang -> trapperepos
    door(4700, 6000, 800, IV, "v", "start", "inn", gulv=FLIS)             # wc/bad
    door(8100, 6000, 800, IV, "v", "end", "ut", gulv=PARKETT)             # sov D <- gardnisje
    door(6900, 6000, 800, IV, "v", "start", "inn", gulv=PARKETT)          # gardnisje
    # trapp
    trapp(3100, 6400, 1500, 2200, opp="s", trinn=9, tekst_under=False)
    tekst(3850, 6200, "NED", 170, GRAA, 500)
    # møblering
    seng(500, 700, 1600, 2000); garderobe(2750, 300, 700, 550)            # sov A
    seng(9000, 700, 1600, 2000); garderobe(7650, 300, 700, 550)           # sov B
    seng(600, 6300, 1600, 2000); garderobe(2200, 9000, 700, 550)          # sov C
    seng(9300, 5700, 1600, 2000)                                          # sov D
    sofa(4100, 2200, 2600, 950)                                           # loftstue
    bord(4800, 1150, 1100, 620, rx=150)
    # gang + bod
    teppe(2700, 4150, 4200, 650)
    hylle(300, 3700, 550, 1400)
    # bad 6,1
    badekar(9350, 3650, 1600, 720)
    vask(8750, 3950, 160)
    toalett(8600, 4700, "s")
    # wc/bad 6,7
    dusj(4900, 5600, 850)
    vask(6100, 5750, 160)
    toalett(5000, 7150, "s")
    # gardnisje + nisje sør
    garderobe(7050, 5600, 550, 1900)
    garderobe(5000, 8200, 1700, 550)
    # balkongmøbler
    bord(1600, -830, 700, 600, rx=120); stol(900, -800); stol(2450, -800)
    stol(9800, 8500); bord(10450, 8400, 700, 700, rx=350)
    # romnavn
    romnavn(1800, 2700, "Soverom", 12.4, s1=280, s2=210)
    tekst(5550, 1750, "Stue", 300, MORK, 600); tekst(5550, 2080, "12,4 m²", 220, GRAA, 400)
    romnavn(9300, 2700, "Soverom", 12.4, s1=280, s2=210)
    tekst(1150, 4600, "Bod 3,5 m²", 200, GRAA, 500)
    tekst(4500, 4850, "Gang 8,6 m²", 240, MORK, 600)
    romnavn(1500, 8600, "Soverom", 12.4, s1=280, s2=210)
    romnavn(9700, 7300, "Soverom", 12.4, s1=250, s2=190)
    tekst(10050, 4900, "Bad 6,1 m²", 220, MORK, 600)
    tekst(5900, 6900, "WC/Bad", 230, MORK, 600); tekst(5900, 7160, "6,7 m²", 180, GRAA, 400)
    tekst(3300, -650, "Balkong 11 m²", 240, GRAA, 600)
    tekst(9000, 9300, "Balkong", 220, "#FDFBF7", 600)
    tekst(9000, 10250, "Balkong 9,9 m²", 220, GRAA, 600)
    sone(1500, -1600, "2. ETASJE")
    skriv("2. etasje", "-700 -2300 13000 13900", (-500, 11000))


etg1()
etg2()
