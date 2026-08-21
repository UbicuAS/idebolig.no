# -*- coding: utf-8 -*-
"""Møblerte 2D-plantegninger for Alva (katalogmodell) — to etasjer, tegnet fra
CAD-skjermbildene Marius sendte 21.08.2026. Ortogonalisert framstilling av den
roterte planen; arealer fra tegningens romlabels.
1.etg: Kjøkken 17,1 / Stue 41,8 / Bod 2,6 / Bod-Tek 7,2 / Gang 8,2 / Bad 6,9 /
Soverom 10 / Terrasse 16,9.  2.etg: 4x Soverom 12,4 / Stue 12,4 / Gang 8,6 /
Bod 3,5 / Bad 6,1 / WC-Bad 6,7 / Walk-in 4,7 / Balkong 11 + 9,9."""
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


def skriv(navn, viewbox, tittel):
    tx, ty = tittel
    tekst(tx, ty, f"Alva — {navn}", 380, MORK, 600, anker="start")
    fil = Path(MAPPE) / f"alva-{navn.replace('. ', '').replace(' ', '-').lower()}.svg"
    svg = HODE.replace("{VB}", viewbox) + "\n".join(alva_helpers.deler) + "\n</svg>\n"
    fil.write_text(svg, encoding="utf-8")
    print("skrev", fil, len(svg))
    alva_helpers.deler.clear()


# ================================================================ 1. ETASJE
# 10600 x 9800. Terrasse vest, inngang sør i gangen.
def etg1():
    alva_helpers.deler.append(
        '<path d="M 0 0 H 10600 V 9800 H 0 Z" fill="#FDFBF7" filter="url(#skygge)"/>')
    # utedekker
    r(-3000, 0, 3000, 5600, "url(#dekke)")
    alva_helpers.deler.append(
        f'<rect x="-3000" y="0" width="3000" height="5600" fill="none" '
        f'stroke="{GRAA}" stroke-width="26" stroke-dasharray="240 140"/>')
    r(6300, 9800, 1600, 1200, "url(#dekke)")                # inngangsrepos sør
    # gulv
    r(0, 0, 10600, 9800, "url(#parkett)")
    r(7900, 2700, 2700, 2700, "url(#flis)")                 # bad
    # yttervegger
    r(0, 0, 10600, YV, MORK)
    r(0, 0, YV, 9800, MORK)
    r(0, 9800 - YV, 10600, YV, MORK)
    r(10600 - YV, 0, YV, 9800, MORK)
    # innervegger
    r(6300, 0, IV, 4100, MORK)                              # kjøkken/stue | høyre kolonne
    r(6300, 5200, IV, 4600, MORK)                           # stue | gang (nedre)
    r(7900, 0, IV, 9800, MORK)                              # midtvegg høyre kolonne
    r(6300, 1700, 1600, IV, MORK)                           # bod 2,6 sør
    r(7900, 2700, 2700, IV, MORK)                           # bod/tek | bad
    r(7900, 5400, 2700, IV, MORK)                           # bad | soverom
    # vinduer
    vindu(1200, 0, 1300, "h")                               # kjøkken nord
    vindu(4700, 0, 1200, "h")                               # stueflik nord
    vindu(0, 1500, 1300, "v")                               # kjøkken vest (mot terrasse)
    vindu(0, 7300, 1500, "v")                               # stue vest
    vindu(1500, 9800 - YV, 1500, "h")                       # stue sør
    vindu(4200, 9800 - YV, 1300, "h")                       # stue sør 2
    vindu(8500, 9800 - YV, 1300, "h")                       # soverom sør
    vindu(10600 - YV, 6800, 1300, "v")                      # soverom øst
    vindu(10600 - YV, 3600, 900, "v")                       # bad øst
    vindu(9200, 0, 1100, "h")                               # bod/tek nord
    # dører
    door(0, 4300, 900, YV, "v", "start", "inn", gulv=PARKETT)             # terrassedør fra stue
    door(6600, 9800 - YV, 1000, YV, "h", "start", "inn", gulv=PARKETT)    # inngang sør (gang)
    r(6300, 4300, IV, 900, "url(#parkett)")                               # åpning stue <-> gang
    door(6300, 400, 800, IV, "v", "start", "ut", gulv=PARKETT)            # bod 2,6 (fra kjøkken)
    door(7900, 1900, 700, IV, "v", "start", "inn", gulv=PARKETT)          # bod/tek (fra trapperom)
    door(7900, 3600, 800, IV, "v", "start", "inn", gulv=FLIS)             # bad (fra gang? nei, fra trapperom)
    door(7900, 8500, 890, IV, "v", "start", "inn", gulv=PARKETT)          # soverom
    # trapp
    trapp(6500, 1800, 1400, 2300, opp="n", trinn=10, tekst_under=False)
    tekst(7200, 4600, "OPP", 170, GRAA, 500)
    # kjøkken
    hylle(YV, YV, 4150, 650)
    komfyr(1000, YV + 60, 520)
    vask(3200, YV + 330, 170)
    bord(3700, 950, 700, 700, rx=30, fyll=MOEBEL)           # kjøl
    # stue: spisegruppe i øvre flik + sofagruppe nede
    bord(4600, 1500, 1200, 2000, rx=200)
    for sy in (1650, 2450):
        stol(4050, sy); stol(5900, sy)
    stol(4900, 990); stol(4900, 3560)
    sofa(700, 8250, 2900, 1000)
    bord(1500, 7200, 1100, 650, rx=200)
    teppe(900, 7000, 3300, 1150)
    hylle(5750, 7400, 420, 1800)                            # tv-benk mot gangvegg
    # gang
    teppe(6700, 8700, 900, 700)
    hylle(6450, 5600, 420, 1400)
    # bad
    dusj(8100, 2950, 850)
    vask(9700, 3300, 160)
    toalett(9900, 4550, "s")
    # bod/tek
    vaskemaskin(8100, 350); vaskemaskin(8750, 350)
    alva_helpers.deler.append(
        f'<circle cx="{10000}" cy="{2100}" r="330" fill="{MOEBEL}" '
        f'stroke="{MOEBEL_K}" stroke-width="20"/>')
    tekst(10000, 2170, "VV", 170, MOEBEL_K, 600)
    hylle(8750, 2050, 700, 420)
    # soverom
    seng(8300, 5800, 1600, 2000)
    nattbord(10050, 5830)
    garderobe(9800, 8300, 550, 1200)
    # bod 2,6
    hylle(6500, 300, 420, 1200)
    # romnavn
    romnavn(2200, 2600, "Kjøkken", 17.1)
    romnavn(3200, 5400, "Stue", 41.8)
    tekst(7100, 1150, "Bod", 200, MORK, 600); tekst(7100, 1390, "2,6 m²", 160, GRAA, 400)
    tekst(9250, 1300, "Bod/Tek.", 230, MORK, 600); tekst(9250, 1560, "7,2 m²", 180, GRAA, 400)
    romnavn(7100, 7500, "Gang", 8.2, s1=260, s2=200)
    romnavn(8900, 4300, "Bad", 6.9, s1=260, s2=200)
    romnavn(9100, 8100, "Soverom", 10, s1=260, s2=200)
    tekst(-1500, 2600, "Terrasse", 260, GRAA, 600)
    tekst(-1500, 2900, "16,9 m²", 200, GRAA, 400)
    tekst(7100, 10700, "Inngang", 220, GRAA, 500)
    sone(1500, -350, "1. ETASJE")
    skriv("1. etasje", "-3700 -1100 15300 13000", (-3500, 11600))


# ================================================================ 2. ETASJE
def etg2():
    alva_helpers.deler.append(
        '<path d="M 0 0 H 10600 V 9800 H 0 Z" fill="#FDFBF7" filter="url(#skygge)"/>')
    # balkonger
    r(0, -2600, 4200, 2600, "url(#dekke)")
    alva_helpers.deler.append(
        f'<rect x="0" y="-2600" width="4200" height="2600" fill="none" '
        f'stroke="{GRAA}" stroke-width="26" stroke-dasharray="240 140"/>')
    r(6400, 9800, 4200, 2200, "url(#dekke)")
    alva_helpers.deler.append(
        f'<rect x="6400" y="9800" width="4200" height="2200" fill="none" '
        f'stroke="{GRAA}" stroke-width="26" stroke-dasharray="240 140"/>')
    # gulv
    r(0, 0, 10600, 9800, "url(#parkett)")
    r(7100, 0, 3500, 3450, "url(#flis)") if False else None
    r(7100, 0, 3500, 1900, "none") if False else None
    r(7100, 0, 3500, 3450, "url(#parkett)")
    r(7100, 0, 3500, 1900, "url(#flis)") if False else None
    # bad-gulv: Bad 6,1 øverst høyre og WC/Bad 6,7 under
    r(7100, 0, 3500, 3450, "url(#flis)")
    r(7100, 3450, 3500, 1950, "url(#flis)")
    # yttervegger
    r(0, 0, 10600, YV, MORK)
    r(0, 0, YV, 9800, MORK)
    r(0, 9800 - YV, 10600, YV, MORK)
    r(10600 - YV, 0, YV, 9800, MORK)
    # innervegger
    r(3550, 0, IV, 3450, MORK)                              # sov tv | sov midt
    r(7100, 0, IV, 5400, MORK)                              # | bad-kolonne
    r(7100, 3450, 3500, IV, MORK)                           # bad 6,1 | wc/bad
    r(0, 3450, 7100, IV, MORK)                              # topprad sør
    r(2000, 3450, IV, 1950, MORK)                           # bod | gang
    r(0, 5400, 10600, IV, MORK)                             # midtbånd sør
    r(3550, 5400, IV, 4400, MORK)                           # sov bv | stue
    r(6400, 5400, IV, 4400, MORK)                           # stue | trapp/walk-in
    r(8100, 5400, IV, 4400, MORK)                           # trapp/walk-in | sov bh
    r(6400, 7700, 1700, IV, MORK)                           # trapp | walk-in
    # vinduer
    vindu(1200, 0, 1300, "h") if False else None
    vindu(5000, 0, 1300, "h")                               # sov midt nord
    vindu(8600, 0, 900, "h")                                # bad 6,1 nord
    vindu(0, 1200, 1300, "v")                               # sov tv vest
    vindu(0, 6800, 1300, "v")                               # sov bv vest
    vindu(1100, 9800 - YV, 1500, "h")                       # sov bv sør
    vindu(4400, 9800 - YV, 1300, "h")                       # stue sør
    vindu(10600 - YV, 4200, 900, "v")                       # wc/bad øst
    vindu(10600 - YV, 6600, 1300, "v")                      # sov bh øst
    # dører
    door(2000, -0 + 0, 0, YV, "h") if False else None
    door(2100, 0, 900, YV, "h", "start", "inn", gulv=DEKKE)               # balkongdør sov tv
    door(8700, 9800 - YV, 900, YV, "h", "start", "ut", gulv=DEKKE)        # balkongdør sov bh
    door(600, 3450, 890, IV, "h", "end", "ut", gulv=PARKETT)              # sov tv
    door(4100, 3450, 890, IV, "h", "start", "ut", gulv=PARKETT)           # sov midt
    door(7100, 700, 800, IV, "v", "start", "inn", gulv=FLIS)              # bad 6,1
    door(7100, 4000, 800, IV, "v", "start", "inn", gulv=FLIS)             # wc/bad
    door(2000, 4400, 800, IV, "v", "end", "ut", gulv=PARKETT)             # bod
    door(900, 5400, 890, IV, "h", "start", "inn", gulv=PARKETT)           # sov bv
    door(4300, 5400, 890, IV, "h", "start", "inn", gulv=PARKETT)          # stue (loftstue)
    door(8100, 7900, 890, IV, "v", "start", "inn", gulv=PARKETT)          # sov bh
    door(8100, 8900, 800, IV, "v", "end", "ut", gulv=PARKETT)             # walk-in (fra sov bh)
    r(6450, 5400, 1550, IV, "url(#parkett)")                              # åpning gang -> trapp
    # trapp
    trapp(6550, 5600, 1400, 2000, opp="s", trinn=9, tekst_under=False)
    tekst(6900, 5320, "NED", 170, GRAA, 500)
    # møblering — soverom
    seng(500, 700, 1600, 2000); garderobe(2650, 300, 750, 550)            # sov tv
    seng(4400, 550, 1600, 2000); garderobe(6250, 300, 700, 550)           # sov midt
    seng(700, 6200, 1600, 2000); garderobe(2700, 9000, 700, 550)          # sov bv
    seng(8750, 5800, 1600, 2000); nattbord(8280, 5830)                    # sov bh
    # loftstue
    sofa(3800, 8500, 2300, 950)
    bord(4400, 7500, 1000, 620, rx=150)
    teppe(3900, 7300, 2200, 1000)
    # gang + bod
    teppe(2600, 4100, 3800, 650)
    hylle(300, 3700, 550, 1400)                                           # bod-hylle
    # bad 6,1
    badekar(8000, 300, 1700, 750)
    vask(10050, 700, 160)
    toalett(9950, 2700, "s")
    # wc/bad 6,7
    dusj(9550, 3700, 850)
    vask(8600, 3800, 160)
    toalett(8150, 4700, "s")
    # walk-in
    garderobe(6550, 7900, 550, 1800)
    # balkongmøbler
    bord(1300, -1700, 850, 850, rx=425)
    stol(600, -1500); stol(2400, -1900)
    sofa(7000, 10200, 2300, 900)
    # romnavn
    romnavn(1750, 2800, "Soverom", 12.4, s1=280, s2=210)
    romnavn(5300, 2800, "Soverom", 12.4, s1=280, s2=210)
    romnavn(1750, 8600, "Soverom", 12.4, s1=280, s2=210)
    romnavn(9350, 8700, "Soverom", 12.4, s1=280, s2=210)
    romnavn(5000, 6600, "Stue", 12.4, s1=280, s2=210)
    tekst(4300, 4850, "Gang 8,6 m²", 240, MORK, 600)
    tekst(1450, 4050, "Bod 3,5 m²", 200, GRAA, 500)
    tekst(8850, 1500, "Bad", 260, MORK, 600); tekst(8850, 1790, "6,1 m²", 200, GRAA, 400)
    tekst(9650, 4980, "WC/Bad", 240, MORK, 600); tekst(9650, 5250, "6,7 m²", 190, GRAA, 400)
    tekst(7500, 8300, "Walk-in", 200, MORK, 600); tekst(7500, 8530, "4,7 m²", 160, GRAA, 400)
    tekst(2100, -1000, "Balkong 11 m²", 230, GRAA, 600)
    tekst(9300, 11300, "Balkong 9,9 m²", 230, GRAA, 600)
    sone(1500, -3000, "2. ETASJE")
    skriv("2. etasje", "-700 -3700 12100 16600", (-500, 12500))


etg1()
etg2()
