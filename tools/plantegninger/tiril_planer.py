# -*- coding: utf-8 -*-
"""Tiril (tomannsbolig) — 2. etasje, fra CAD-skjermbildet 21.08.2026 +
fasadebildet Fasade-fremside.webp (2025/06). To speilvendte enheter om
midtaksen; per enhet: master soverom m/ walk-in og stort bad (12,2),
kontor/soverom, to soverom, gang m/ trappehus i utstikk på gavlen, balkong
bak (11,9) og foran (9,8 / 7,8) med tett trerekkverk (fasadefasit).
1. etasje tegnes når grunnlaget kommer. Front tegnes nederst (sør)."""
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

B = 16000    # total bredde (to enheter à 8000)
D = 10600
M = 8000     # midtakse


def skriv(navn, viewbox, tittel):
    tx, ty = tittel
    tekst(tx, ty, f"Tiril — {navn}", 380, MORK, 600, anker="start")
    fil = Path(MAPPE) / f"tiril-{navn.replace('. ', '').replace(' ', '-').lower()}.svg"
    svg = HODE.replace("{VB}", viewbox) + "\n".join(alva_helpers.deler) + "\n</svg>\n"
    fil.write_text(svg, encoding="utf-8")
    print("skrev", fil, len(svg))
    alva_helpers.deler.clear()


def rekkverk_h(x1, y, x2):
    """Tett trerekkverk (fasadefasit): kraftig dobbel strek."""
    linje(x1, y, x2, y, MORK, 70)
    linje(x1, y + 110, x2, y + 110, "#6B5B45", 40)


class Enhet:
    def __init__(self, speil):
        self.s = speil

    def X(self, x, w=0):
        return (B - x - w) if self.s else x

    def r(self, x, y, w, h, *a, **k):
        r(self.X(x, w), y, w, h, *a, **k)

    def vindu_h(self, x, y, lengde):
        vindu(self.X(x, lengde), y, lengde, "h")

    def vindu_v(self, x, y, lengde):
        vindu(self.X(x, YV), y, lengde, "v")

    def door_h(self, x, y, bredde, veggT, hengsel, sving, gulv="#FDFBF7"):
        h2 = hengsel if not self.s else ("end" if hengsel == "start" else "start")
        door(self.X(x, bredde), y, bredde, veggT, "h", h2, sving, gulv)

    def door_v(self, x, y, bredde, veggT, hengsel, sving, gulv="#FDFBF7"):
        sv = sving if not self.s else ("ut" if sving == "inn" else "inn")
        door(self.X(x, veggT), y, bredde, veggT, "v", hengsel, sv, gulv)

    def tekst(self, x, y, s, *a, **k):
        tekst(self.X(x), y, s, *a, **k)

    def romnavn(self, x, y, navn, areal=None, **k):
        romnavn(self.X(x), y, navn, areal, **k)


def enhet2(E: Enhet, balkong_foran: float):
    # --- balkonger (tett trerekkverk)
    E.r(600, -2600, 4400, 2600, "url(#dekke)")
    rekkverk_h(E.X(600, 4400), -2710, E.X(600, 4400) + 4400)
    linje(E.X(600, 0), -2600, E.X(600, 0), 0, MORK, 50)
    linje(E.X(5000, 0), -2600, E.X(5000, 0), 0, MORK, 50)
    E.tekst(2800, -1200, "Balkong 11,9 m²", 230, GRAA, 600)
    bord(E.X(1400, 800), -2000, 800, 800, rx=400)
    stol(E.X(2400, 420), -1800); stol(E.X(900, 420), -1150)
    E.r(2000, D, 4000, 2400, "url(#dekke)")
    rekkverk_h(E.X(2000, 4000), D + 2400, E.X(2000, 4000) + 4000)
    linje(E.X(2000, 0), D, E.X(2000, 0), D + 2510, MORK, 50)
    linje(E.X(6000, 0), D, E.X(6000, 0), D + 2510, MORK, 50)
    E.tekst(4000, D + 1350, f"Balkong {balkong_foran} m²", 230, GRAA, 600)
    stol(E.X(2700, 420), D + 700); stol(E.X(3500, 420), D + 700)
    # --- trappehus-utstikk på gavlen
    E.r(-1500, 4400, 1500 + YV, 3200, "url(#parkett)")
    E.r(-1500, 4400, 1500, YV, MORK)
    E.r(-1500, 7600 - YV, 1500, YV, MORK)
    E.r(-1500, 4400, YV, 3200, MORK)
    tr_x = E.X(-1400, 1300)
    trapp(tr_x, 4750, 1300, 2500, opp="s", trinn=9, tekst_under=False)
    E.tekst(-700, 4200, "NED", 160, GRAA, 500)
    # --- gulvsoner
    E.r(4600, 3800, 3400, 3600, "url(#flis)")               # bad 12,2
    # --- innervegger
    E.r(2400, 0, IV, 2400, MORK)                            # walk-in | master-sone
    E.r(0, 2400, 2400 + IV, IV, MORK)                       # walk-in | kontor
    E.r(2400, 2400, IV, 3200, MORK)                         # kontor | gang
    E.r(0, 5600, 2400 + IV, IV, MORK)                       # kontor sør
    E.r(4000, 0, IV, 3800, MORK)                            # gang/walk-in | master
    E.r(4000, 3800 - IV, 4000, IV, MORK)                    # master | bad
    E.r(4600, 3800, IV, 3600, MORK)                         # gang | bad
    E.r(0, 7400, 8000, IV, MORK)                            # midtbånd | soverom (m/ åpninger)
    E.r(3300, 7400, IV, 3200, MORK)                         # sov 11,8 | korridor
    E.r(4400, 7400, IV, 3200, MORK)                         # korridor | sov 13,1
    # --- vinduer og dører i yttervegg
    E.door_h(4300, 0, 900, YV, "start", "inn", gulv=DEKKE)  # master -> balkong bak
    E.vindu_h(1000, 0, 1300)                                # walk-in bak
    E.vindu_v(0, 3300, 1300)                                # kontor gavl
    E.vindu_v(0, 8400, 1400)                                # sov 11,8 gavl
    E.vindu_h(700, D - YV, 1400)                            # sov 11,8 front
    E.door_h(4800, D - YV, 900, YV, "start", "inn", gulv=DEKKE)  # sov 13,1 -> balkong foran
    E.vindu_h(6300, D - YV, 1300)                           # sov 13,1 front
    # --- dører innvendig
    E.door_h(600, 2400, 800, IV, "start", "ut", gulv=PARKETT)      # walk-in (fra kontor? nei gang)
    E.door_v(2400, 900, 800, IV, "start", "ut", gulv=PARKETT)      # walk-in <- gangsonen
    E.door_v(2400, 3400, 890, IV, "start", "ut", gulv=PARKETT)     # kontor <- gang
    E.door_v(4000, 1400, 890, IV, "end", "inn", gulv=PARKETT)      # master <- gang
    E.door_v(4600, 4600, 800, IV, "start", "inn", gulv=FLIS)       # bad <- gang
    E.r(2500, 7400, 700, IV, "url(#parkett)")                      # åpning gang -> korridor? nei:
    E.r(3400, 7400, 900, IV, "url(#parkett)")                      # åpning gang -> sovekorridor
    E.door_h(700, 7400, 890, IV, "start", "ut", gulv=PARKETT)      # sov 11,8
    E.door_h(4700, 7400, 890, IV, "start", "ut", gulv=PARKETT)     # sov 13,1
    r(E.X(0, YV) if E.s else -0, 0, 0, 0, "none")
    # --- åpning gang -> trappehus
    E.r(0, 4900, YV, 2200, "url(#parkett)")
    # --- møblering
    garderobe(E.X(300, 550), 300, 550, 1700)                       # walk-in
    garderobe(E.X(1600, 700), 300, 700, 550)
    mobel_rect(E.X(300, 1400), 3000, 1400, 600, rx=40)             # kontor: pult
    stol(E.X(800, 420), 3700)
    hylle(E.X(300, 450), 4600, 450, 800)
    seng(E.X(5300, 1800), 700, 1800, 2100)                         # master (mot midtveggen)
    nattbord(E.X(4800, 420), 730)
    badekar(E.X(5600, 1700), 4100, 1700, 750)                      # bad
    vask(E.X(5200), 6300, 160); vask(E.X(6000), 6300, 160)
    toalett(E.X(7300, 420), 6700, "s")
    teppe(E.X(2700, 1600), 5300, 1600, 1600)                       # gang
    seng(E.X(700, 1600), 8100, 1600, 2000)                         # sov 11,8
    garderobe(E.X(2600, 550), 8000, 550, 1500)
    seng(E.X(5500, 1600), 7700, 1600, 2000)                        # sov 13,1 (mot midten)
    garderobe(E.X(4600, 550), 9000, 550, 1400)
    # --- romnavn
    E.tekst(1200, 1500, "Walk-in", 200, MORK, 600)
    E.tekst(1200, 1730, "5,6 m²", 160, GRAA, 400)
    E.tekst(1200, 4400, "Kontor/Sov", 200, MORK, 600)
    E.tekst(1200, 4630, "7,6 m²", 160, GRAA, 400)
    E.romnavn(6000, 2600, "Master soverom", 15.2, s1=240, s2=190)
    E.tekst(6300, 5000, "Bad", 240, MORK, 600)
    E.tekst(6300, 5270, "12,2 m²", 190, GRAA, 400)
    E.tekst(3400, 6600, "Gang", 220, MORK, 600)
    E.tekst(3400, 6840, "15,4 m²", 170, GRAA, 400)
    E.romnavn(1650, 9600, "Soverom", 11.8, s1=250, s2=200)
    E.romnavn(6100, 9300, "Soverom", 13.1, s1=250, s2=200)


# Enklere: tegn alt i riktig rekkefølge i én omgang i stedet.
def bygg():
    alva_helpers.deler.clear()
    alva_helpers.deler.append(
        f'<path d="M 0 0 H {B} V {D} H 0 Z" fill="#FDFBF7" filter="url(#skygge)"/>')
    alva_helpers.deler.append(
        f'<rect x="0" y="0" width="{B}" height="{D}" fill="url(#parkett)"/>')
    r(0, 0, B, YV, MORK)
    r(0, 0, YV, D, MORK)
    r(B - YV, 0, YV, D, MORK)
    r(0, D - YV, B, YV, MORK)
    for speil in (False, True):
        enhet2(Enhet(speil), 9.8 if not speil else 7.8)
    r(M - IV, 0, IV + IV, D, MORK)
    sone(1500, -3100, "2. ETASJE · TO ENHETER")
    skriv("2. etasje", "-2600 -3800 21400 18100", (-2400, 13900))


bygg()
