# -*- coding: utf-8 -*-
"""Nora — 2. etasje (1. etasje-tegning mangler ennå). Fra CAD-skjermbildet
21.08.2026 + fasadebildene Fasade-Nora / Fasade-bakside-Nora:
- Loftstue i egen vinge mot hagen med dobbelhøy glassgavl; feltet «ÅPENT NED»
  er galleri over 1. etasje (tegnes som åpning med rekkverk).
- Fire soverom, kontor og bad rundt midtsonen; trapp ved galleriet.
- Utstikket foran i CAD-en er VALMTAKET over inngangen (fasadefasit) —
  tegnes som stiplet takkontur, ingen balkong.
Front tegnes nederst (sør); stuevingen bak (nord)."""
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

B, D0, D1 = 13600, 2800, 10200      # kropp x0..B, y D0..D1; vinge y0..D0
VX1, VX2 = 4400, 8600               # stuevingen (bak-midt)


def skriv(navn, viewbox, tittel):
    tx, ty = tittel
    tekst(tx, ty, f"Nora — {navn}", 380, MORK, 600, anker="start")
    fil = Path(MAPPE) / f"nora-{navn.replace('. ', '').replace(' ', '-').lower()}.svg"
    svg = HODE.replace("{VB}", viewbox) + "\n".join(alva_helpers.deler) + "\n</svg>\n"
    fil.write_text(svg, encoding="utf-8")
    print("skrev", fil, len(svg))
    alva_helpers.deler.clear()


def etg2():
    alva_helpers.deler.append(
        f'<path d="M 0 {D0} H {VX1} V 0 H {VX2} V {D0} H {B} V {D1} H 0 Z" '
        'fill="#FDFBF7" filter="url(#skygge)"/>')
    # valmtak over inngangen (stiplet — fasadefasit, ikke balkong)
    tx1, tx2, ty2 = 5400, 8200, D1 + 1400
    alva_helpers.deler.append(
        f'<rect x="{tx1}" y="{D1}" width="{tx2 - tx1}" height="{ty2 - D1}" '
        f'fill="none" stroke="{GRAA}" stroke-width="24" stroke-dasharray="180 110"/>')
    linje(tx1, D1, (tx1 + tx2) / 2, ty2, GRAA, 16, dash="140 90")
    linje(tx2, D1, (tx1 + tx2) / 2, ty2, GRAA, 16, dash="140 90")
    tekst((tx1 + tx2) / 2, ty2 + 350, "Tak over inngang", 190, GRAA, 500)
    # gulv
    r(0, D0, B, D1 - D0, "url(#parkett)")
    r(VX1, 0, VX2 - VX1, D0, "url(#parkett)")
    r(10600, 5400, 3000, 1800, "url(#flis)")                # bad 6,5
    # ÅPENT NED (galleri over 1. etasje)
    r(5400, 6900, 2600, 3050, "#F1ECE1")
    alva_helpers.deler.append(
        '<rect x="5400" y="6900" width="2600" height="3050" fill="none" '
        f'stroke="{GRAA}" stroke-width="22" stroke-dasharray="150 100"/>')
    linje(5400, 6900, 8000, 9950, GRAA, 14)
    linje(8000, 6900, 5400, 9950, GRAA, 14)
    linje(5400, 6900 + 40, 8000, 6900 + 40, MORK, 44)       # rekkverk mot gangen
    tekst(6700, 8350, "Åpent ned", 230, GRAA, 500)
    # yttervegger (m/ vinge)
    r(0, D0, VX1 + IV, YV, MORK)
    r(VX2 - IV, D0, B - VX2 + IV, YV, MORK)
    r(VX1, 0, YV, D0 + YV, MORK)
    r(VX2 - YV, 0, YV, D0 + YV, MORK)
    r(VX1, 0, VX2 - VX1, YV, MORK)
    r(0, D0, YV, D1 - D0, MORK)
    r(B - YV, D0, YV, D1 - D0, MORK)
    r(0, D1 - YV, B, YV, MORK)
    # innervegger
    r(4200, D0, IV, 2800, MORK)                             # sov 17 | stuevinge-sone
    r(0, 5600, 4200 + IV, IV, MORK)                         # sov 17 sør
    r(2600, 5600, IV, 1700, MORK)                           # kontor øst
    r(0, 7300, 2600 + IV, IV, MORK)                         # kontor sør
    r(0, 7300, 4200 + IV, IV, MORK) if False else None
    r(2600, 7300 - IV, 1600 + IV, IV, MORK)                 # sov 15 nord (østre del)
    r(4200, 7300, IV, 2900, MORK)                           # sov 15 øst
    r(9000, D0, IV, 2600, MORK)                             # gang | sov 12
    r(9000, 5400 - IV, 4600, IV, MORK)                      # sov 12 sør
    r(10600, 5400, IV, 1800, MORK)                          # gang | bad
    r(9000, 7200, 4600, IV, MORK)                           # bad | sov 14
    r(9000, 7200, IV, 3000, MORK)                           # gang | sov 14
    # vinduer
    vindu(VX1 + 500, 0, 1400, "h")                          # stuevinge glassgavl
    vindu(VX1 + 2300, 0, 1400, "h")                         # stuevinge glassgavl 2
    vindu(0, 3600, 1400, "v")                               # sov 17 vestgavl
    vindu(0, 6100, 900, "v")                                # kontor vest
    vindu(0, 8200, 1400, "v")                               # sov 15 vest
    vindu(1200, D1 - YV, 1400, "h")                         # sov 15 front
    vindu(9800, D1 - YV, 1400, "h")                         # sov 14 front
    vindu(B - YV, 3400, 1400, "v")                          # sov 12 østgavl
    vindu(B - YV, 6000, 800, "v")                           # bad øst
    vindu(B - YV, 8100, 1400, "v")                          # sov 14 øst
    vindu(900, D0, 1300, "h")                               # sov 17 bak
    vindu(10200, D0, 1300, "h")                             # sov 12 bak
    # dører
    door(2900, 5600, 890, IV, "h", "end", "ut", gulv=PARKETT)       # sov 17
    door(2600, 6100, 800, IV, "v", "start", "ut", gulv=PARKETT)     # kontor
    door(3100, 7300 - IV, 890, IV + IV, "h", "start", "ut", gulv=PARKETT)  # sov 15
    door(9000, 3400, 890, IV, "v", "start", "ut", gulv=PARKETT)     # sov 12
    door(10600, 6000, 800, IV, "v", "start", "inn", gulv=FLIS)      # bad
    door(9000, 7800, 890, IV, "v", "start", "ut", gulv=PARKETT)     # sov 14
    # trapp (ned) ved galleriet
    trapp(4300, 7400, 1000, 2500, opp="s", trinn=9, tekst_under=False)
    tekst(4800, 7200, "NED", 160, GRAA, 500)
    # LOFTSTUE i vingen
    sofa(VX1 + 500, 600, 2600, 950)
    bord(VX1 + 1300, 1800, 1100, 620, rx=150)
    teppe(VX1 + 700, 1650, 2700, 950)
    # møblering rom
    seng(500, 3200, 1700, 2050); nattbord(2400, 3230)               # sov 17
    garderobe(3400, 3000, 700, 550)
    mobel_rect(300, 5800, 1400, 600, rx=40); stol(900, 6500)        # kontor: pult
    seng(700, 7800, 1600, 2000); garderobe(3400, 9400, 700, 550)    # sov 15
    seng(11200, 3000, 1700, 2050); nattbord(10400, 3030)            # sov 12
    dusj(10800, 5600, 800)                                          # bad
    vask(12200, 5800, 150)
    toalett(12900, 6500, "s")
    seng(11300, 7700, 1600, 2000); garderobe(9300, 9400, 800, 550)  # sov 14
    teppe(6000, 4200, 2600, 900)                                    # gangsone
    # romnavn
    tekst(6500, 1500, "Stue", 300, MORK, 600)
    romnavn(2100, 4400, "Soverom", 16.7, s1=270, s2=210)
    tekst(1900, 6900, "Kontor", 210, MORK, 600); tekst(1900, 7130, "6,4 m²", 165, GRAA, 400)
    romnavn(2100, 8600, "Soverom", 14.6, s1=270, s2=210)
    romnavn(11300, 4400, "Soverom", 14.1, s1=270, s2=210)
    tekst(11800, 6900, "Bad", 230, MORK, 600); tekst(12500, 6900, "6,5 m²", 180, GRAA, 400) if False else tekst(11800, 7120, "6,5 m²", 180, GRAA, 400)
    romnavn(11300, 8700, "Soverom", 15.4, s1=270, s2=210)
    tekst(6800, 5600, "Gang", 230, GRAA, 500)
    sone(1500, 2100, "2. ETASJE")
    skriv("2. etasje", "-700 -900 15200 13800", (-500, 12100))



# ================================================================ 1. ETASJE
# Fra CAD 21.08 (rom 01-09): Entré 24,2 m/ trapp og galleri over («Åpent
# ned» i 2. etg), Kjøkken 46,2, Spisestue 33,3 i vingen m/ glassgavl,
# Stue 18,4, Bad 12,6, Vaskerom 14; Terrasse (åpen) i vinkelen ved vingen
# og INNGLASSET terrasse langs vestfasaden (begge «not enclosed»).
def etg1():
    alva_helpers.deler.append(
        f'<path d="M 0 {D0} H {VX1} V 0 H {VX2} V {D0} H {B} V {D1} H 0 Z" '
        'fill="#FDFBF7" filter="url(#skygge)"/>')
    # valmtak over inngangen (stiplet)
    tx1, tx2, ty2 = 5700, 8500, D1 + 1300
    alva_helpers.deler.append(
        f'<rect x="{tx1}" y="{D1}" width="{tx2 - tx1}" height="{ty2 - D1}" '
        f'fill="none" stroke="{GRAA}" stroke-width="24" stroke-dasharray="180 110"/>')
    tekst((tx1 + tx2) / 2, ty2 + 350, "Tak over inngang", 190, GRAA, 500)
    # TERRASSE (åpen) i vinkelen vest for vingen
    r(-100, -100, VX1 + 100, D0 + 100, "url(#dekke)")
    tekst(2100, 900, "Terrasse", 250, GRAA, 600)
    bord(700, 1500, 800, 800, rx=400); stol(300, 1250); stol(1650, 1700)
    # INNGLASSET TERRASSE langs vestfasaden
    gx, gy1, gy2 = -3200, D0, 9400
    r(gx, gy1, -gx, gy2 - gy1, "url(#dekke)")
    r(gx, gy1, -gx, 120, MORK); r(gx, gy2 - 120, -gx, 120, MORK)
    r(gx, gy1, 120, gy2 - gy1, MORK)
    for yy in range(gy1 + 500, gy2 - 700, 1500):
        linje(gx + 40, yy, gx + 40, yy + 1100, "#FDFBF7", 40)
    tekst(gx / 2, 5800, "Innglasset", 230, GRAA, 600)
    tekst(gx / 2, 6100, "terrasse", 230, GRAA, 600)
    sofa(gx + 300, 3200, 2300, 900)
    bord(gx + 900, 4400, 1000, 600, rx=150)
    # gulv
    r(0, D0, B, D1 - D0, "url(#parkett)")
    r(VX1, 0, VX2 - VX1, D0, "url(#parkett)")
    r(9000, 6600, 4600, 3600, "url(#flis)")                 # bad + vaskerom
    # yttervegger
    r(0, D0, VX1 + IV, YV, MORK)
    r(VX2 - IV, D0, B - VX2 + IV, YV, MORK)
    r(VX1, 0, YV, D0 + YV, MORK)
    r(VX2 - YV, 0, YV, D0 + YV, MORK)
    r(VX1, 0, VX2 - VX1, YV, MORK)
    r(0, D0, YV, D1 - D0, MORK)
    r(B - YV, D0, YV, D1 - D0, MORK)
    r(0, D1 - YV, B, YV, MORK)
    # innervegger
    r(4400, 6600, IV, 3600, MORK)                           # kjøkken | entré (nedre)
    r(9000, D0, IV, 800, MORK)                              # spisestue | stue (kort vange)
    r(9000, 6600, 4600, IV, MORK)                           # stue | bad-sone
    r(9000, 6600, IV, 3600, MORK)                           # entré | bad/vask
    r(9000, 8400, 4600, IV, MORK)                           # bad | vaskerom
    r(4400, 6600, 4600 + IV, IV, MORK)                      # spisestue/stue | entré (m/ åpning)
    # vinduer og dører i yttervegg
    vindu(VX1 + 500, 0, 1400, "h")                          # spisestue glassgavl
    vindu(VX1 + 2300, 0, 1400, "h")                         # spisestue glassgavl 2
    door(VX1, 900, 900, YV, "v", "start", "ut", gulv=PARKETT)      # spisestue -> terrassen
    door(0, 4400, 900, YV, "v", "start", "ut", gulv=PARKETT)       # kjøkken -> innglasset terrasse
    vindu(0, 6500, 1400, "v")                               # kjøkken vest
    vindu(1400, D1 - YV, 1600, "h")                         # kjøkken front
    door(6700, D1 - YV, 1000, YV, "h", "start", "inn")      # HOVEDINNGANG
    vindu(10200, D1 - YV, 1100, "h")                        # vaskerom front
    vindu(B - YV, 8800, 900, "v")                           # vaskerom øst
    vindu(B - YV, 7000, 900, "v")                           # bad øst
    vindu(B - YV, 3800, 1600, "v")                          # stue østgavl
    vindu(9800, D0, 1400, "h")                              # stue bak
    vindu(900, D0, 1400, "h")                               # kjøkken bak (mot terrassen)
    # dører innvendig
    r(5000, 6600, 1400, IV, "url(#parkett)")                # åpning spisestue -> entré
    r(4400, 8000, IV, 1400, "url(#parkett)")                # åpning kjøkken -> entré
    door(9000, 7000, 800, IV, "v", "start", "inn", gulv=FLIS)      # entré -> bad
    door(9000, 8800, 800, IV, "v", "start", "inn", gulv=FLIS)      # entré -> vaskerom
    r(9000, 4200, IV, 2400, "url(#parkett)")                # åpen overgang spisestue/stue
    # trapp (opp) + galleri-markering over entré
    trapp(4600, 7400, 1000, 2500, opp="n", trinn=9, tekst_under=False)
    tekst(5100, 7200, "OPP", 160, GRAA, 500)
    alva_helpers.deler.append(
        '<rect x="5700" y="6900" width="2600" height="3050" fill="none" '
        f'stroke="{GRAA}" stroke-width="18" stroke-dasharray="120 90"/>')
    tekst(7000, 8000, "Galleri over", 180, GRAA, 500)
    # KJØKKEN 46,2
    hylle(300, 3000, 620, 2600)                             # benk vest
    komfyr(320, 3900, 500)
    hylle(300, 9200, 3400, 620)                             # benk front
    vask(2400, 9500, 160)
    hylle(1700, 5600, 1900, 750)                            # kjøkkenøy
    bord(2500, 7300, 1500, 900, rx=120)                     # frokostbord
    stol(2650, 6830); stol(3400, 6830)
    # SPISESTUE 33,3 (vingen)
    bord(5600, 900, 1800, 1100, rx=150)
    stol(5750, 430); stol(6550, 430); stol(5750, 2050); stol(6550, 2050)
    teppe(5300, 3300, 3200, 1000)
    mobel_rect(8200, 3000, 550, 1600)                       # skjenk
    # STUE 18,4
    sofa(9600, 3300, 2700, 950)
    bord(10400, 4600, 1100, 620, rx=200)
    teppe(9800, 4400, 2900, 1000)
    hylle(11000, 2900, 1800, 420)                           # tv-benk mot bakvegg
    # ENTRÉ 24,2
    teppe(6600, 9300, 1400, 600)
    garderobe(8100, 9300, 800, 550)
    # BAD 12,6
    badekar(9300, 6800, 1700, 750)
    dusj(12500, 6800, 850)
    vask(11500, 7000, 160)
    toalett(12900, 7700, "s") if False else toalett(11900, 7700, "s")
    # VASKEROM 14
    vaskemaskin(9300, 8700); vaskemaskin(9950, 8700)
    hylle(12200, 8700, 1200, 450)
    alva_helpers.deler.append(
        f'<circle cx="13000" cy="9600" r="300" fill="{MOEBEL}" '
        f'stroke="{MOEBEL_K}" stroke-width="20"/>')
    tekst(13000, 9670, "VV", 160, MOEBEL_K, 600)
    # romnavn
    romnavn(2300, 4900, "Kjøkken", 46.2)
    romnavn(6700, 5300, "Spisestue", 33.3, s1=280, s2=210)
    romnavn(11300, 5600, "Stue", 18.4, s1=280, s2=210)
    romnavn(7000, 9000, "Entré", 24.2, s1=260, s2=200)
    tekst(11700, 7550, "Bad", 240, MORK, 600); tekst(11700, 7820, "12,6 m²", 190, GRAA, 400)
    romnavn(11300, 9500, "Vaskerom", 14, s1=250, s2=200)
    sone(-2600, 1600, "1. ETASJE")
    skriv("1. etasje", "-3900 -900 18400 13800", (-3700, 12100))


etg1()
etg2()
