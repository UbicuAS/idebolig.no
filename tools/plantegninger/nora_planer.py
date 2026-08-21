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


etg2()
