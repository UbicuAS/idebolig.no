# -*- coding: utf-8 -*-
"""Møblerte 2D-plantegninger for Embla (4-mannsbolig) — to etasjer, tegnet fra
CAD-skjermbildene Marius sendte 21.08.2026 + fasadebildet Fasade-fremside.webp.

To speilvendte leiligheter per etasje om midtaksen; terrasse (21,4) / balkong
(13,4) side om side langs FRONTEN med stakittrekkverk; liten terrasse (8,5) /
balkong (7,1) på baksiden ved soverommene; felles trappe-/heisvolum stikker ut
bak i midten (Felles gang 24,3 / 20,2). Front tegnes nederst (sør)."""
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

B = 17600    # total bredde (to leiligheter à 8800)
D = 11000    # dybde
M = 8800     # midtakse


def skriv(navn, viewbox, tittel):
    tx, ty = tittel
    tekst(tx, ty, f"Embla — {navn}", 380, MORK, 600, anker="start")
    fil = Path(MAPPE) / f"embla-{navn.replace('. ', '').replace(' ', '-').lower()}.svg"
    svg = HODE.replace("{VB}", viewbox) + "\n".join(alva_helpers.deler) + "\n</svg>\n"
    fil.write_text(svg, encoding="utf-8")
    print("skrev", fil, len(svg))
    alva_helpers.deler.clear()


def rekkverk_h(x1, y, x2):
    linje(x1, y, x2, y, MORK, 40)
    linje(x1, y + 70, x2, y + 70, GRAA, 22)


class Leil:
    """Tegner én leilighet; speil=True speiler om midtaksen x=M."""

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


def leilighet(L: Leil, etg: int):
    stue_areal = 20.8 if etg == 1 else 22.1
    kjk_areal = 15 if etg == 1 else 13.7
    # --- gulvsoner
    L.r(6300, 5100, 2500, 2300, "url(#flis)")       # bad 6,7
    # --- innervegger (lokalt 0..8800; y0=bak, y11000=front)
    L.r(3700, 0, IV, 3450, MORK)                    # sov 12,7 | sov 8,9
    L.r(6300, 0, IV, 3450 + IV, MORK)               # sov 8,9 | vf/bod
    L.r(6300, 1650, 1600 + IV, IV, MORK)            # vf | bod
    L.r(7900, 1650, IV, 1800, MORK)                 # bod | korridor
    L.r(0, 3450, 7900, IV, MORK)                    # sovrad | gang (m/ åpning øst)
    L.r(1500, 3450, IV, 1650, MORK)                 # stueflik | gang
    L.r(0, 5100, 6300, IV, MORK)                    # gang | stue (m/ åpning)
    L.r(6300, 5100, IV, 2300, MORK)                 # gang/stue | bad vest
    L.r(6300, 7400 - IV, 2500, IV, MORK)            # bad | kjøkken
    # --- vinduer og skyvedører
    L.vindu_h(900, 0, 1400)                         # sov 12,7 bak
    L.vindu_v(0, 1300, 1400)                        # sov 12,7 gavl
    L.vindu_v(0, 6300, 1600)                        # stue gavl
    L.vindu_v(0, 8900, 1400)                        # stue gavl 2
    sx = L.X(1200, 1900)
    L.r(1200, D - YV, 1900, YV, "url(#parkett)")    # skyvedør stue -> terrasse
    linje(sx, D - YV / 2, sx + 1900, D - YV / 2, MORK, 30)
    linje(sx, D - 30, sx + 1900, D - 30, MORK, 22)
    L.vindu_h(5400, D - YV, 1400)                   # kjøkken front
    L.door_h(4600, 0, 900, YV, "start", "inn", gulv=PARKETT)   # sov 8,9 -> uteplass bak
    # --- dører innvendig
    L.door_h(6900, 0, 900, YV, "start", "inn", gulv=PARKETT)   # FELLESGANG -> VF
    L.r(7900, 3450, 900, IV, "url(#parkett)")                  # åpning korridor -> gang
    L.door_v(7900, 2300, 800, IV, "start", "ut", gulv=PARKETT) # korridor -> bod
    L.door_h(1800, 3450, 890, IV, "end", "ut", gulv=PARKETT)   # gang -> sov 12,7
    L.door_h(4300, 3450, 890, IV, "start", "ut", gulv=PARKETT) # gang -> sov 8,9
    L.door_h(6700, 5100, 800, IV, "start", "inn", gulv=FLIS)   # gang -> bad
    L.r(1900, 5100, 1600, IV, "url(#parkett)")                 # åpning gang -> stue
    # --- møblering
    seng(L.X(500, 1700), 550, 1700, 2050)           # sov 12,7
    nattbord(L.X(2300, 420), 570)
    garderobe(L.X(2900, 700), 300, 700, 550)
    seng(L.X(4100, 1500), 550, 1500, 2000)          # sov 8,9
    nattbord(L.X(5700, 420), 570)
    teppe(L.X(6600, 900), 350, 900, 900)            # vf-matte
    hylle(L.X(7350, 450), 1800, 450, 1450)          # bodhylle
    vaskemaskin(L.X(6450, 600), 1800, 600)
    dusj(L.X(6550, 850), 5300, 850)                 # bad
    vask(L.X(7900), 5500, 160)
    toalett(L.X(8150, 420), 6650, "s")
    teppe(L.X(2200, 3300), 3900, 3300, 700)         # gangteppe
    sofa(L.X(700, 2600), 8600, 2600, 950)           # stue
    bord(L.X(1600, 1100), 7500, 1100, 650, rx=200)
    teppe(L.X(1300, 2600), 7300, 2600, 1100)
    hylle(L.X(4000, 420), 6500, 420, 1800)          # tv-benk mot gang/stue-vegg
    hylle(L.X(6500, 2100), 7550, 2100, 620)         # kjøkkenbenk mot badveggen
    komfyr(L.X(7350, 500), 7600, 500)
    vask(L.X(6900), 7900, 150)
    bord(L.X(6500, 1500), 9200, 1500, 900, rx=120)  # spisebord
    stol(L.X(6650, 420), 8730); stol(L.X(7400, 420), 8730)
    stol(L.X(6650, 420), 10170); stol(L.X(7400, 420), 10170)
    # --- romnavn
    L.romnavn(2550, 2900, "Soverom", 12.7, s1=240, s2=190)
    L.romnavn(5100, 2900, "Soverom", 8.9, s1=240, s2=190)
    L.tekst(7100, 1250, "VF", 200, MORK, 600); L.tekst(7100, 1480, "4,1 m²", 160, GRAA, 400)
    L.tekst(7080, 2950, "Bod", 200, MORK, 600); L.tekst(7080, 3180, "5,1 m²", 160, GRAA, 400)
    L.tekst(4000, 4500, "Gang 6,1 m²", 220, MORK, 600)
    L.tekst(7550, 6300, "Bad", 240, MORK, 600); L.tekst(7550, 6570, "6,7 m²", 190, GRAA, 400)
    L.romnavn(2100, 7900, "Stue", stue_areal)
    L.romnavn(5300, 10300, "Kjøkken", kjk_areal, s1=270, s2=210)


def uteareal(L: Leil, etg: int):
    if etg == 1:
        L.r(600, D, 7600, 2600, "url(#dekke)")      # terrasse 21,4 front
        rekkverk_h(L.X(600, 7600), D + 2600, L.X(600, 7600) + 7600)
        linje(L.X(600, 0), D, L.X(600, 0), D + 2670, MORK, 40)
        linje(L.X(8200, 0), D, L.X(8200, 0), D + 2670, MORK, 40)
        L.tekst(4300, D + 1500, "Terrasse 21,4 m²", 260, GRAA, 600)
        L.r(2400, -2100, 3900, 2100, "url(#dekke)") # terrasse 8,5 bak
        rekkverk_h(L.X(2400, 3900), -2170, L.X(2400, 3900) + 3900)
        L.tekst(4350, -1000, "Terrasse 8,5 m²", 230, GRAA, 600)
    else:
        L.r(600, D, 7600, 1900, "url(#dekke)")      # balkong 13,4 front
        rekkverk_h(L.X(600, 7600), D + 1900, L.X(600, 7600) + 7600)
        linje(L.X(600, 0), D, L.X(600, 0), D + 1970, MORK, 40)
        linje(L.X(8200, 0), D, L.X(8200, 0), D + 1970, MORK, 40)
        L.tekst(4300, D + 1150, "Balkong 13,4 m²", 260, GRAA, 600)
        L.r(2800, -2000, 3500, 2000, "url(#dekke)") # balkong 7,1 bak
        rekkverk_h(L.X(2800, 3500), -2070, L.X(2800, 3500) + 3500)
        L.tekst(4550, -950, "Balkong 7,1 m²", 230, GRAA, 600)
    # utemøbler på front-uteplassen
    bord(L.X(2500, 800), D + 500, 800, 800, rx=400)
    stol(L.X(1800, 420), D + 650); stol(L.X(3500, 420), D + 650)


def felles(etg: int):
    """Felles trappe-/heisvolum bak i midten."""
    areal = "24,3" if etg == 1 else "20,2"
    fx, fy = M - 2200, -4600
    r(fx, fy, 4400, 4600, "url(#flis)")
    r(fx, fy, 4400, YV, MORK)
    r(fx, fy, YV, 4600, MORK)
    r(fx + 4400 - YV, fy, YV, 4600, MORK)
    r(fx, -YV, 4400, YV, MORK) if False else None
    door(M - 450, fy, 900, YV, "h", "start", "inn", gulv=FLIS)   # felles inngang
    trapp(fx + 500, fy + 900, 1500, 2600, opp="n" if etg == 1 else "s",
          trinn=10, tekst_under=False)
    # heis
    hx = fx + 2600
    r(hx, fy + 900, 1300, 1600, MOEBEL, MOEBEL_K, 26)
    linje(hx, fy + 900, hx + 1300, fy + 2500, MOEBEL_K, 18)
    linje(hx + 1300, fy + 900, hx, fy + 2500, MOEBEL_K, 18)
    tekst(hx + 650, fy + 2900, "Heis", 190, GRAA, 500)
    tekst(M, fy + 4100, f"Felles gang {areal} m²", 230, MORK, 600)
    tekst(M, -4900, "Felles inngang", 200, GRAA, 500)


def etasje(etg: int):
    navn = "1. etasje" if etg == 1 else "2. etasje"
    alva_helpers.deler.append(
        f'<path d="M 0 0 H {B} V {D} H 0 Z" fill="#FDFBF7" filter="url(#skygge)"/>')
    for speil in (False, True):
        uteareal(Leil(speil), etg)
    felles(etg)
    r(0, 0, B, D, "url(#parkett)")
    # yttervegger + midtvegg (leilighetsskille)
    r(0, 0, B, YV, MORK)
    r(0, 0, YV, D, MORK)
    r(B - YV, 0, YV, D, MORK)
    r(0, D - YV, B, YV, MORK)
    for speil in (False, True):
        leilighet(Leil(speil), etg)
    r(M - IV, 0, IV + IV, D, MORK)
    sone(1500, -5200, f"{navn.upper()} · BRA 84 M² PR LEILIGHET")
    skriv(navn, "-700 -5900 19000 19900", (-500, 14700))


etasje(1)
etasje(2)
