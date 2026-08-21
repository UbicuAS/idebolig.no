# -*- coding: utf-8 -*-
"""Møblerte 2D-plantegninger for Odin — to etasjer, fra CAD-skjermbildene
Marius sendte 21.08.2026, kryssjekket mot fasadebildene
(Fasade-fremside-post-prod + Fasade-bakside-post-prod):
- Stor bakkeplan-terrasse med stakittrekkverk foran vestre del av fronten,
  med trapp i vestenden.
- Inngangsutstikk på fronten (Inngang 14,4 m² m/ innvendig trapp) og
  BALKONG 5,5 m² på utstikkets tak, med dør fra gangen i 2. etasje.
- Bakdør fra vaskerommet på østgavlen.
- 2. etasje er loftsetasje: vinduer i gavlene + balkongdør (skråtak mot
  langfasadene). Front tegnes nederst (sør)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from alva_helpers import (MAPPE, MORK, GRAA, GULL, PARKETT, PARKETT_L, FLIS,
                          FLIS_L, DEKKE, DEKKE_L, MOEBEL, MOEBEL_K, YV, IV,
                          r, linje, tekst, romnavn, sone, vindu, door,
                          mobel_rect, seng, nattbord, garderobe, sofa, bord,
                          stol, vask, komfyr, toalett, dusj, badekar,
                          vaskemaskin, teppe, trapp, hylle, HODE)
import alva_helpers

B, D = 14200, 8100          # 1. etg hovedkropp
UX1, UX2 = 5600, 8000       # inngangsutstikk (front-midt)
UD = 1800                   # utstikkets dybde


def skriv(navn, viewbox, tittel):
    tx, ty = tittel
    tekst(tx, ty, f"Odin — {navn}", 380, MORK, 600, anker="start")
    fil = Path(MAPPE) / f"odin-{navn.replace('. ', '').replace(' ', '-').lower()}.svg"
    svg = HODE.replace("{VB}", viewbox) + "\n".join(alva_helpers.deler) + "\n</svg>\n"
    fil.write_text(svg, encoding="utf-8")
    print("skrev", fil, len(svg))
    alva_helpers.deler.clear()


def rekkverk_h(x1, y, x2):
    linje(x1, y, x2, y, MORK, 40)
    linje(x1, y + 70, x2, y + 70, GRAA, 22)


def skyvedor_s(x, y, lengde):
    r(x, y, lengde, YV, "url(#parkett)")
    linje(x, y + YV / 2, x + lengde, y + YV / 2, MORK, 30)
    linje(x, y + YV - 30, x + lengde, y + YV - 30, MORK, 22)


# ================================================================ 1. ETASJE
def etg1():
    alva_helpers.deler.append(
        f'<path d="M 0 0 H {B} V {D} H {UX2} V {D + UD} H {UX1} V {D} H 0 Z" '
        'fill="#FDFBF7" filter="url(#skygge)"/>')
    # TERRASSE foran vestre del (fasadefasit): stort dekk m/ trapp i vestenden
    r(-2300, D, 7300, 2400, "url(#dekke)")
    rekkverk_h(-2300, D + 2400, 5000)
    linje(5000, D, 5000, D + 2470, MORK, 40)
    trapp(-2300, D + 600, 1100, 1500, opp="n", trinn=4, tekst_under=False)
    tekst(1600, D + 1450, "Terrasse", 260, GRAA, 600)
    # gulv
    r(0, 0, B, D, "url(#parkett)")
    r(UX1, D, UX2 - UX1, UD, "url(#parkett)")               # inngangsutstikk
    r(7300, 0, 2500, 3600, "url(#flis)")                    # bad
    r(9800, 0, 4400, 2700, "url(#flis)")                    # vaskerom
    # yttervegger (m/ utstikk)
    r(0, 0, B, YV, MORK)
    r(0, 0, YV, D, MORK)
    r(B - YV, 0, YV, D, MORK)
    r(0, D - YV, UX1 + IV, YV, MORK)
    r(UX2 - IV, D - YV, B - UX2 + IV, YV, MORK)
    r(UX1, D, YV, UD, MORK)
    r(UX2 - YV, D, YV, UD, MORK)
    r(UX1, D + UD - YV, UX2 - UX1, YV, MORK)
    # innervegger
    r(3600, 0, IV, 3600, MORK)                              # stue | soverom
    r(3600, 3600 - IV, 6200 + IV, IV, MORK)                 # bakrad | front (m/ åpninger)
    r(7300, 0, IV, 3600, MORK)                              # soverom | bad
    r(9800, 0, IV, 3600, MORK)                              # bad | vask/kjøkken
    r(9800, 2700, 4400, IV, MORK)                           # vaskerom | kjøkken
    r(5600, 3600, IV, 4500, MORK)                           # stue | inngangssone
    r(8000, 3600, IV, 4500, MORK)                           # inngang | gang
    r(9800, 3600, IV, 1500, MORK)                           # gang | kjøkken (øvre del)
    # vinduer + dører i yttervegg
    vindu(0, 1600, 1600, "v")                               # stue vestgavl
    vindu(0, 4700, 1600, "v")                               # stue vestgavl 2
    skyvedor_s(1500, D - YV, 1800)                          # stue -> terrassen
    vindu(4900, 0, 1400, "h")                               # soverom bak
    vindu(8100, 0, 900, "h")                                # bad bak (lite)
    vindu(11500, 0, 1100, "h")                              # vaskerom bak
    door(B - YV, 900, 900, YV, "v", "start", "ut", gulv=FLIS)   # bakdør østgavl (vaskerom)
    vindu(B - YV, 4500, 1400, "v")                          # kjøkken østgavl
    vindu(10900, D - YV, 1500, "h")                         # kjøkken front
    door(6300, D + UD - YV, 1000, YV, "h", "start", "inn")  # HOVEDINNGANG (utstikket)
    # dører innvendig
    r(4200, 3600 - IV, 1000, IV + IV, "url(#parkett)")      # åpning stue -> bakre sone? nei: sov-dør:
    door(6000, 3600 - IV, 890, IV + IV, "h", "start", "ut", gulv=PARKETT)   # soverom (fra gangsonen)
    door(8500, 3600 - IV, 800, IV + IV, "h", "start", "ut", gulv=FLIS)      # bad (fra gang)
    door(10800, 2700, 800, IV, "h", "start", "ut", gulv=FLIS)               # vaskerom (fra kjøkken)
    r(5600, 4600, IV, 1200, "url(#parkett)")                # åpning stue <-> inngangssone
    r(8000, 4600, IV, 1200, "url(#parkett)")                # åpning inngang <-> gang
    r(9800, 5100, IV, 2900, "url(#parkett)")                # åpen overgang gang <-> kjøkken
    # trapp (i gangen, opp)
    trapp(8300, 6300, 1500, 1800, opp="n", trinn=8, tekst_under=False)
    tekst(9050, 6100, "OPP", 170, GRAA, 500)
    # STUE
    sofa(500, 5700, 2700, 1000)
    bord(1400, 4600, 1100, 650, rx=200)
    teppe(700, 4400, 2800, 1100)
    hylle(4900, 4600, 420, 1900)                            # tv-benk mot inngangsvegg
    bord(900, 1200, 2000, 1000, rx=200)                     # spisegruppe ved gavlvinduet
    stol(1100, 740); stol(1900, 740); stol(1100, 2260); stol(1900, 2260)
    # SOVEROM 13,1
    seng(4200, 500, 1700, 2050)
    nattbord(6300, 530)
    garderobe(4100, 2900, 1900, 550)
    # BAD 8,7
    dusj(7500, 300, 850)
    badekar(8900, 1500, 750, 1600) if False else None
    vask(9300, 700, 160)
    toalett(9200, 2750, "s")
    vaskemaskin(7500, 2800, 600) if False else None
    # VASKEROM 11
    vaskemaskin(10200, 350); vaskemaskin(10850, 350)
    hylle(12200, 300, 1700, 450)
    alva_helpers.deler.append(
        f'<circle cx="13600" cy="2100" r="320" fill="{MOEBEL}" '
        f'stroke="{MOEBEL_K}" stroke-width="20"/>')
    tekst(13600, 2170, "VV", 170, MOEBEL_K, 600)
    # KJØKKEN 20
    hylle(10100, 2900, 4000, 620)                           # benk mot vaskeromsveggen
    komfyr(11200, 2950, 500)
    vask(12800, 3200, 160)
    bord(11000, 5300, 2200, 1100, rx=150)                   # spisebord
    stol(11250, 4830); stol(12050, 4830); stol(11250, 6400); stol(12050, 6400)
    # INNGANG 14,4
    teppe(6300, 7300, 1300, 600)
    garderobe(5800, 4000, 550, 1500)
    mobel_rect(7300, 4000, 550, 1200)                       # skohylle
    # romnavn
    romnavn(2100, 3200, "Stue", 28.8)
    romnavn(5600, 3000, "Soverom", 13.1, s1=250, s2=195)
    tekst(8500, 1900, "Bad", 240, MORK, 600); tekst(8500, 2170, "8,7 m²", 190, GRAA, 400)
    romnavn(12000, 1500, "Vaskerom", 11, s1=250, s2=200)
    romnavn(12300, 4400, "Kjøkken", 20, s1=270, s2=210)
    romnavn(6800, 6300, "Inngang", 14.4, s1=250, s2=200)
    tekst(8900, 4300, "Gang", 230, MORK, 600); tekst(8900, 4560, "10,9 m²", 180, GRAA, 400)
    sone(1500, -700, "1. ETASJE")
    skriv("1. etasje", "-3000 -1400 18500 13400", (-2800, 11400))


# ================================================================ 2. ETASJE
# Loftsetasje: mindre kropp, vinduer i gavlene, balkong på utstikkstaket.
def etg2():
    K0, K1, KD = 1000, 13200, 6600          # kropp x0..x1, dybde
    alva_helpers.deler.append(
        f'<path d="M {K0} 0 H {K1} V {KD} H {K0} Z" fill="#FDFBF7" filter="url(#skygge)"/>')
    # BALKONG 5,5 på inngangsutstikkets tak
    r(UX1, KD, UX2 - UX1, 1800, "url(#dekke)")
    rekkverk_h(UX1, KD + 1800, UX2)
    linje(UX1, KD, UX1, KD + 1870, MORK, 40)
    linje(UX2, KD, UX2, KD + 1870, MORK, 40)
    tekst((UX1 + UX2) / 2, KD + 2350, "Balkong 5,5 m²", 230, GRAA, 600)
    # gulv
    r(K0, 0, K1 - K0, KD, "url(#parkett)")
    r(5500, 0, 2400, 3300, "url(#flis)")                    # bad 7,1
    # yttervegger
    r(K0, 0, K1 - K0, YV, MORK)
    r(K0, 0, YV, KD, MORK)
    r(K1 - YV, 0, YV, KD, MORK)
    r(K0, KD - YV, K1 - K0, YV, MORK)
    # innervegger
    r(4300, 0, IV, 3300, MORK)                              # sov A | kott
    r(5500, 0, IV, 3300, MORK)                              # kott | bad
    r(4300, 2000, 1200 + IV, IV, MORK)                      # kott sør
    r(7900, 0, IV, 3800, MORK)                              # bad/gang | sov C
    r(K0, 3300, 3300 + IV, IV, MORK)                        # sov A | sov B
    r(4300, 3300, 3600 + IV, IV, MORK)                      # bakrad | gang (m/ dører)
    r(7900, 3800 - IV, 5300, IV, MORK)                      # sov C sør
    r(4300, 3300, IV, 3300, MORK)                           # sov B | gang
    # vinduer (kun gavler + balkongdør — loftsetasje)
    vindu(K0, 900, 1300, "v")                               # sov A vestgavl
    vindu(K0, 4400, 1300, "v")                              # sov B vestgavl
    vindu(K1 - YV, 900, 1300, "v")                          # sov C østgavl
    vindu(K1 - YV, 4600, 1300, "v")                         # sov C/gang østgavl
    door(6300, KD - YV, 900, YV, "h", "start", "ut", gulv=DEKKE)   # balkongdør fra gangen
    # dører innvendig
    door(3600, 3300, 700, IV, "h", "end", "ut", gulv=PARKETT) if False else None
    door(1500, 3300, 890, IV, "h", "start", "inn", gulv=PARKETT) if False else None
    door(4300, 700, 0, IV, "v") if False else None
    door(4300, 2450, 800, IV, "v", "start", "ut", gulv=PARKETT)    # sov B? nei: sov A/gang-passasje
    r(4300, 2450, IV, 850, "url(#parkett)") if False else None
    door(4700, 2000, 700, IV, "h", "start", "ut", gulv=PARKETT)    # kott (fra gangen)
    door(6300, 3300, 800, IV, "h", "start", "ut", gulv=FLIS)       # bad (fra gangen)
    door(8600, 3800 - IV, 890, IV, "h", "start", "ut", gulv=PARKETT)  # sov C (fra gangen)
    door(4300, 4400, 890, IV, "v", "start", "ut", gulv=PARKETT)    # sov B (fra gangen)
    door(3000, 3300, 890, IV, "h", "end", "ut", gulv=PARKETT)      # sov A (fra gangen)
    # trapp (ned)
    trapp(8300, 4900, 1500, 1700, opp="s", trinn=8, tekst_under=False)
    tekst(9050, 4700, "NED", 170, GRAA, 500)
    # møblering
    seng(1400, 500, 1600, 2000); nattbord(3120, 520)               # sov A
    garderobe(3400, 1700, 700, 550)
    seng(1400, 3900, 1600, 2000); nattbord(3120, 3920)             # sov B
    garderobe(3450, 5900, 700, 550)
    seng(10200, 500, 1700, 2050); nattbord(9500, 530)              # sov C
    garderobe(12300, 2900, 700, 550)
    hylle(4450, 350, 450, 1300)                                    # kott-hylle
    dusj(5700, 300, 850)                                           # bad
    vask(7300, 700, 160)
    toalett(7300, 2450, "s")
    teppe(4900, 4300, 2800, 700)                                   # gangteppe
    # romnavn
    romnavn(2450, 2900, "Soverom", 10.5, s1=250, s2=195)
    romnavn(2450, 6250, "Soverom", 10.5, s1=250, s2=195)
    tekst(5150, 2750, "Kott", 180, MORK, 600); tekst(5150, 2960, "2,3 m²", 145, GRAA, 400)
    tekst(6650, 2000, "Bad", 240, MORK, 600); tekst(6650, 2270, "7,1 m²", 190, GRAA, 400)
    romnavn(9600, 3050, "Soverom", 15.2, s1=250, s2=195)
    tekst(6100, 5500, "Gang 22,3 m²", 250, MORK, 600)
    sone(2500, -700, "2. ETASJE")
    skriv("2. etasje", "-1000 -1400 16000 11500", (-800, 9700))


etg1()
etg2()
