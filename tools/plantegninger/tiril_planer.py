# -*- coding: utf-8 -*-
"""Tiril (tomannsbolig, moderne) — begge etasjer, tegnet fra
«Tiril - 2mannsbolig moderne.pdf» (målsatt arkitekttegning).

Rutenett fra PDF: akse 1 = x 0, akse 2 = x 7550 (midtvegg/leilighetsskille),
akse 3 = x 15100. Trappehusene stikker 1100 ut på hver gavl.
Akse A = y 0 (bakside: garasjer og innganger), E = y 14550 (hagesiden).

Uterommene (feilkilden i tre tidligere forsøk):
- BAK: terrasse 8,7 (1. etg) og balkong 11,9/11,8 (2. etg) er INNTRUKKET i
  byggets fotavtrykk ved gavlene — de stikker ikke ut.
- FORAN: terrasse 24,6/24,5 (1. etg) og balkong 9,8/7,8 (2. etg) stikker ut
  med SKRÅ framkant som møtes i en spiss ved midtaksen.
Front (hagesiden) tegnes nederst."""
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

M = 7550        # midtakse (leilighetsskille)
B = 15100       # bygningsbredde
D = 14550       # bygningsdybde
UT = 1100       # trappehusenes utstikk på gavlene
A, AB, AD = 0, 2550, 7850     # akser i dybderetning
HX = 3400       # hakk i sørveggen: kjøkken/soverom stikker ut hit
HD1, HD2 = 1250, 997    # hakkets dybde i 1. og 2. etasje (PDF)


def skriv(navn, viewbox, tittel):
    tx, ty = tittel
    tekst(tx, ty, f"Tiril — {navn}", 380, MORK, 600, anker="start")
    fil = Path(MAPPE) / f"tiril-{navn.replace('. ', '').replace(' ', '-').lower()}.svg"
    svg = HODE.replace("{VB}", viewbox) + "\n".join(alva_helpers.deler) + "\n</svg>\n"
    fil.write_text(svg, encoding="utf-8")
    print("skrev", fil, len(svg))
    alva_helpers.deler.clear()


class E:
    """Én enhet; speil=True speiler om midtaksen."""

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

    def seng(self, x, y, bredde, lengde, mot):
        """Seng inntil vegg; 'mot' speiles sammen med posisjonen."""
        m2 = mot if not self.s else {"v": "h", "h": "v"}.get(mot, mot)
        w = bredde if mot in ("n", "s") else lengde
        seng_r(self.X(x, w), y, bredde, lengde, m2)

    def poly(self, pts, fill):
        d = "M " + " L ".join(f"{self.X(x)} {y}" for x, y in pts) + " Z"
        alva_helpers.deler.append(f'<path d="{d}" fill="{fill}"/>')

    def kant(self, pts, sw=70):
        d = "M " + " L ".join(f"{self.X(x)} {y}" for x, y in pts)
        alva_helpers.deler.append(
            f'<path d="{d}" fill="none" stroke="{MORK}" stroke-width="{sw}"/>')

    def skyvedor_s(self, x, lengde):
        self.r(x, D - YV, lengde, YV, "url(#parkett)")
        x0 = self.X(x, lengde)
        linje(x0, D - YV / 2, x0 + lengde, D - YV / 2, MORK, 30)
        linje(x0, D - 30, x0 + lengde, D - 30, MORK, 22)

    def trappehus(self, opp):
        """Trappehus i utstikket på gavlen (1100 mm ut)."""
        self.r(-UT, AD, UT + YV, 2900, "url(#parkett)")
        self.r(-UT, AD, UT, YV, MORK)
        self.r(-UT, AD + 2900 - YV, UT, YV, MORK)
        self.r(-UT, AD, YV, 2900, MORK)
        trapp(self.X(-UT + 150, 800), AD + 350, 800, 2200, opp=opp,
              trinn=9, tekst_under=False)
        self.tekst(-UT + 500, AD - 250, "OPP" if opp == "n" else "NED",
                   170, GRAA, 500)
        self.r(0, AD + 800, YV, 1400, "url(#parkett)")



def seng_r(x, y, bredde, lengde, mot):
    """Seng der hodegjerdet ligger inntil veggen i retning `mot`
    ('n' = vegg over, 's' = under, 'v' = til venstre, 'h' = til høyre).
    bredde = sengebredde, lengde = sengelengde."""
    if mot in ("n", "s"):
        w, h = bredde, lengde
    else:
        w, h = lengde, bredde
    mobel_rect(x, y, w, h, rx=60)
    if mot == "n":
        linje(x, y + 140, x + w, y + 140, MOEBEL_K, 20)
        pw = (w - 240) / 2
        r(x + 80, y + 220, pw, 340, "#F3EDE2", MOEBEL_K, 18, rx=70)
        r(x + 160 + pw, y + 220, pw, 340, "#F3EDE2", MOEBEL_K, 18, rx=70)
        r(x + 60, y + 700, w - 120, h - 780, "#F6F1E7", MOEBEL_K, 18, rx=50)
    elif mot == "s":
        linje(x, y + h - 140, x + w, y + h - 140, MOEBEL_K, 20)
        pw = (w - 240) / 2
        r(x + 80, y + h - 560, pw, 340, "#F3EDE2", MOEBEL_K, 18, rx=70)
        r(x + 160 + pw, y + h - 560, pw, 340, "#F3EDE2", MOEBEL_K, 18, rx=70)
        r(x + 60, y + 80, w - 120, h - 780, "#F6F1E7", MOEBEL_K, 18, rx=50)
    elif mot == "v":
        linje(x + 140, y, x + 140, y + h, MOEBEL_K, 20)
        ph = (h - 240) / 2
        r(x + 220, y + 80, 340, ph, "#F3EDE2", MOEBEL_K, 18, rx=70)
        r(x + 220, y + 160 + ph, 340, ph, "#F3EDE2", MOEBEL_K, 18, rx=70)
        r(x + 700, y + 60, w - 780, h - 120, "#F6F1E7", MOEBEL_K, 18, rx=50)
    else:  # 'h'
        linje(x + w - 140, y, x + w - 140, y + h, MOEBEL_K, 20)
        ph = (h - 240) / 2
        r(x + w - 560, y + 80, 340, ph, "#F3EDE2", MOEBEL_K, 18, rx=70)
        r(x + w - 560, y + 160 + ph, 340, ph, "#F3EDE2", MOEBEL_K, 18, rx=70)
        r(x + 80, y + 60, w - 780, h - 120, "#F6F1E7", MOEBEL_K, 18, rx=50)


def front_uterom(e: E, hx, hd, d_gavl, d_midt, etikett, tekst_y, helbredde):
    """Terrasse/balkong foran, målt ut av arkitekt-PDF-ens vektorer.

    Sørveggen har et HAKK ved x=hx: soveroms-/kjøkkendelen mot gavlen står
    framme ved D, resten er trukket inn til D-hd. Ytterkanten er én rett
    SKRÅ linje fra (0, D+d_gavl) til (M, D+d_midt), felles for begge
    enhetene, så den danner en spiss ved midtaksen.
    helbredde=True (terrassen på bakkeplan) dekker hele enhetsbredden;
    helbredde=False (balkongen) ligger KUN i det inntrukne partiet."""
    def yk(x):
        return d_gavl + x / M * (d_midt - d_gavl)
    if helbredde:
        e.poly([(0, D), (hx, D), (hx, D - hd), (M, D - hd),
                (M, D + d_midt), (0, D + d_gavl)], "url(#dekke)")
    else:
        e.poly([(hx, D - hd), (M, D - hd), (M, D + d_midt),
                (hx, D + yk(hx))], "url(#dekke)")
        # ytterkanten fortsetter som takutstikk langs den framskutte delen
        e.kant([(0, D + d_gavl), (hx, D + yk(hx))], sw=26)
    e.kant([(hx, D + yk(hx)), (M, D + d_midt)])
    e.tekst(M - 2400, D + tekst_y, etikett, 200, GRAA, 600)


# ================================================================ 1. ETASJE
def etg1(e: E, terr_for, kjokkenstue, d_midt):
    # terrasse FORAN: (1000+5500)/2 x 7550 = 24,5 m²
    front_uterom(e, HX, HD1, 1500, d_midt, f"Terrasse {terr_for} m²", 1150, True)
    bord(e.X(5100, 1700), D + 1500, 1700, 950, rx=120)
    for sx in (5300, 6200):
        stol(e.X(sx, 400), D + 1000); stol(e.X(sx, 400), D + 2550)
    # --- gulv
    e.r(0, A, M, D, "url(#parkett)")
    e.r(3400, A, M - 3400, 5450, "url(#betong)")            # garasje
    e.r(0, 5650, 2150, AD - 5650, "url(#flis)")             # WC
    e.r(3400, 5450, M - 3400, 1350, "url(#flis)")           # teknisk
    e.r(0, A, 3400, AB, "url(#dekke)")                      # terrasse bak (inntrukket)
    e.tekst(2600, 1600, "Terrasse", 195, GRAA, 600)
    e.tekst(2600, 1840, "8,7 m²", 160, GRAA, 400)
    bord(e.X(1100, 700), 800, 700, 700, rx=350); stol(e.X(2150, 400), 950)
    # --- yttervegger
    e.r(3400, A, M - 3400, YV, MORK)                        # nordvegg (garasjen)
    e.r(0, AB, YV, D - AB, MORK)                            # vestvegg (fra VF og ned)
    e.r(0, D - YV, HX, YV, MORK)                            # sørvegg, framskutt del
    e.r(HX, D - HD1 - YV, M - HX, YV, MORK)                 # sørvegg, inntrukket del
    e.r(HX - YV, D - HD1 - YV, YV, HD1 + YV, MORK)          # hakkets vange
    # terrassen ved gavlen er ÅPEN — ingen yttervegg, kun dekke-/takkant
    e.kant([(0, AB), (0, A), (3400, A)], sw=26)
    # --- innervegger
    e.r(3400, A, IV, 6800, MORK)
    e.r(0, AB, 3400 + IV, IV, MORK)                         # terrasse | VF
    e.r(0, 5650, 2150 + IV, IV, MORK)                       # VF | WC
    e.r(2150, 5650, IV, AD - 5650, MORK)
    e.r(3400, 5450, M - 3400, IV, MORK)                     # garasje | teknisk
    e.r(0, AD, M, IV, MORK)                                 # øvre sone | kjøkken/stue
    # --- porter, dører, åpninger
    e.r(4100, A, 2800, YV, "#FDFBF7")                       # garasjeport
    x0 = e.X(4100, 2800)
    linje(x0, A + 40, x0 + 2800, A + 40, MORK, 34)
    linje(x0, A + YV - 40, x0 + 2800, A + YV - 40, MORK, 34, dash="200 120")
    e.door_h(700, AB, 900, IV, "start", "inn", gulv=PARKETT)    # terrasse -> VF
    e.r(3400, 3100, IV, 1100, "url(#betong)")                   # VF <-> garasje
    e.door_v(2150, 6050, 800, IV, "start", "inn", gulv=FLIS)    # WC
    e.door_h(5300, 5450, 800, IV, "start", "ut", gulv=FLIS)     # teknisk
    e.r(800, AD, 1900, IV, "url(#parkett)")                     # VF -> kjøkken/stue
    e.door_h(4800, AD, 900, IV, "start", "ut", gulv=PARKETT)    # teknisk -> stue
    e.trappehus("n")
    e.skyvedor_s(1500, 2200); e.skyvedor_s(4700, 2200)
    e.vindu_v(0, 3300, 1400)                                # VF gavl
    e.vindu_v(0, 11200, 1600)                               # stue gavl
    # --- møblering
    e.tekst(5500, 2500, "Garasje", 230, MORK, 600)
    e.tekst(5500, 2760, "22,6 m²", 180, GRAA, 400)
    e.tekst(5500, 3080, "Betonggulv", 155, GRAA, 400)
    teppe(e.X(1200, 1500), 3500, 1500, 900)
    garderobe(e.X(2700, 550), 4900, 550, 1400)
    toalett(e.X(250, 420), 5950, "n")
    vask(e.X(1500), 7500, 150)
    vaskemaskin(e.X(3600, 600), 5720); vaskemaskin(e.X(4300, 600), 5720)
    hylle(e.X(6300, 1100), 5700, 1100, 420)
    hylle(e.X(150, 700), 9300, 700, 3100)                   # kjøkkenbenk
    komfyr(e.X(200, 500), 9700, 500)
    vask(e.X(500), 11500, 160)
    hylle(e.X(1600, 2400), 9300, 2400, 700)                 # kjøkkenøy
    bord(e.X(3800, 2400), 9700, 2400, 1100, rx=130)
    for sx in (4000, 4900, 5800):
        stol(e.X(sx, 400), 9220); stol(e.X(sx, 400), 10900)
    sofa(e.X(1400, 3000), 12800, 3000, 1000)
    bord(e.X(2400, 1200), 11700, 1200, 700, rx=200)
    teppe(e.X(1700, 3100), 11500, 3100, 1250)
    hylle(e.X(5700, 450), 12200, 450, 1900)
    # --- romnavn
    e.tekst(1700, 4500, "VF", 220, MORK, 600)
    e.tekst(1700, 4750, "10,6 m²", 170, GRAA, 400)
    e.tekst(1050, 7150, "WC", 195, MORK, 600)
    e.tekst(1050, 7380, "4,7 m²", 158, GRAA, 400)
    e.tekst(5450, 6050, "Teknisk/Sportsbod", 180, MORK, 600)
    e.tekst(5450, 6290, "5,6 m²", 155, GRAA, 400)
    e.romnavn(3600, 11400, "Kjøkken/stue", kjokkenstue, s1=285, s2=215)


# ================================================================ 2. ETASJE
def etg2(e: E, bal_bak, bal_for, sov14, master, walkin, gang):
    # Balkongdekket gaar HELT UT TIL GAVLEN (smalt der soverommet staar
    # framme, bredt i det inntrukne partiet) — ikke avskaaret ved hakket.
    hx = 3196 if not e.s else 4201
    front_uterom(e, hx, HD2, 419, 1592, f"Balkong {bal_for} m²", 600, True)
    # --- gulv
    e.r(0, A, M, D, "url(#parkett)")
    e.r(4400, 5150, M - 4400, 3850, "url(#flis)")           # bad
    e.r(0, A, 4650, AB, "url(#dekke)")                      # balkong bak (inntrukket)
    e.tekst(3600, 1500, "Balkong", 200, GRAA, 600)
    e.tekst(3600, 1740, f"{bal_bak} m²", 165, GRAA, 400)
    bord(e.X(1500, 800), 700, 800, 800, rx=400)
    stol(e.X(2650, 400), 850); stol(e.X(650, 400), 1700)
    # --- yttervegger
    e.r(4650, A, M - 4650, YV, MORK)                        # nordvegg (master)
    e.r(4650, A, YV, AB + IV, MORK)                         # vegg balkong | master
    e.r(0, AB, 4650 + YV, YV, MORK)                         # vegg balkong | walk-in
    e.r(0, AB, YV, D - AB, MORK)                            # vestvegg (fra walk-in og ned)
    # balkongen ved gavlen er ÅPEN — kun rekkverk/dekkekant
    e.kant([(0, AB), (0, A), (4650, A)], sw=26)
    e.r(0, D - YV, hx, YV, MORK)                            # sørvegg, framskutt del
    e.r(hx, D - HD2 - YV, M - hx, YV, MORK)                 # sørvegg, inntrukket del
    e.r(hx - YV, D - HD2 - YV, YV, HD2 + YV, MORK)          # hakkets vange
    # --- innervegger
    e.r(4400, A, IV, 5150, MORK)
    e.r(2200, AB, IV, 5100 - AB, MORK)                      # walk-in øst
    e.r(0, 5100, 2900 + IV, IV, MORK)                       # walk-in | kontor
    e.r(2900, 5100, IV, 2650, MORK)
    e.r(0, 7750, 2900 + IV, IV, MORK)                       # kontor sør
    e.r(4400, 5150, M - 4400, IV, MORK)                     # master | bad
    e.r(4400, 5150, IV, 3850, MORK)                         # gang | bad
    e.r(4400, 9000, M - 4400, IV, MORK)                     # bad | sov 13,1
    e.r(0, 10550, M, IV, MORK)                              # gang | soveromsrad
    e.r(hx, 10550, IV, D - 10550 - HD2, MORK)
    # --- dører og vinduer
    e.door_h(3400, AB, 900, YV, "start", "ut", gulv=DEKKE)      # gang -> balkong bak
    e.door_v(4400, 800, 900, IV, "end", "inn", gulv=PARKETT)    # master
    e.door_v(2200, 3100, 800, IV, "start", "ut", gulv=PARKETT)  # walk-in
    e.door_h(800, 5100, 890, IV, "start", "ut", gulv=PARKETT)   # kontor
    e.door_v(4400, 6100, 800, IV, "start", "inn", gulv=FLIS)    # bad
    e.door_h(2100, 10550, 890, IV, "start", "inn", gulv=PARKETT)
    e.door_h(hx + 350, 10550, 890, IV, "start", "inn", gulv=PARKETT)
    e.door_h(M - 2000, D - HD2 - YV, 900, YV, "start", "inn", gulv=DEKKE)  # sov -> balkong
    e.trappehus("s")
    e.vindu_v(0, 3100, 1300)                                # walk-in gavl
    e.vindu_v(0, 6200, 1200)                                # kontor gavl
    e.vindu_h(1200, D - YV, 1500)                           # sov v/gavl, sør

    # --- møblering (hodegjerde alltid inntil vegg, klar av dør og vindu)
    # MASTER: hodegjerdet mot nordveggen, nattbord på begge sider
    e.seng(5150, 500, 1800, 2100, "n")
    nattbord(e.X(4700, 420), 520)                          # ved hodeenden
    nattbord(e.X(6980, 420), 520)                          # ved hodeenden
    # WALK-IN: skap langs begge langvegger
    garderobe(e.X(250, 550), AB + 400, 550, 1700)
    garderobe(e.X(1500, 600), AB + 250, 600, 550)
    # KONTOR/SOV: pult mot gavlvinduet, klar av døra
    mobel_rect(e.X(300, 1400), 6600, 1400, 620, rx=40)
    stol(e.X(850, 400), 6100)
    # BAD: badekar mot midtveggen, servanter mot masterveggen
    badekar(e.X(5650, 1700), 5400, 1700, 750)
    vask(e.X(5300), 7250, 160); vask(e.X(6200), 7250, 160)
    toalett(e.X(6950, 420), 8150, "s")
    teppe(e.X(3100, 2100), 8900, 2100, 1400)                # gang
    # SOVEROM v/gavlen: hodegjerdet mot gavlveggen (vest), fri passasje til døra
    e.seng(YV + 80, 11900, 1600, 2000, "v")
    garderobe(e.X(hx - 550, 550), 11900, 550, 1600)        # inntil skilleveggen
    # SOVEROM 13,1: hodegjerdet mot midtveggen (øst), klar av balkongdøra
    e.seng(M - YV - 2100, 11500, 1800, 2100, "h")
    nattbord(e.X(M - YV - 420, 420), 10950)                # ved hodeenden
    # --- romnavn
    e.romnavn(6000, 3300, "Master soverom", master, s1=220, s2=175)
    e.tekst(1150, 3900, "Walk in closet", 180, MORK, 600)
    e.tekst(1150, 4130, f"{walkin} m²", 152, GRAA, 400)
    e.tekst(1550, 7250, "Kontor/Sov", 190, MORK, 600)
    e.tekst(1550, 7490, "7,6 m²", 158, GRAA, 400)
    e.tekst(5950, 8650, "Bad", 230, MORK, 600)
    e.tekst(5950, 8910, "12,2 m²", 182, GRAA, 400)
    e.tekst(3350, 10150, "Gang", 210, MORK, 600)
    e.tekst(3350, 10390, f"{gang} m²", 172, GRAA, 400)
    e.romnavn(1900, 13900, "Soverom", sov14, s1=225, s2=180)
    e.romnavn(hx + 900, 11000, "Soverom", 13.1, s1=225, s2=180)


def bygg(navn, viewbox, tittel, sone_tekst):
    alva_helpers.deler.clear()
    alva_helpers.deler.append(
        f'<path d="M 0 0 H {B} V {D} H 0 Z" fill="#FDFBF7" filter="url(#skygge)"/>')
    if navn == "1. etasje":
        etg1(E(False), 24.6, 42.3, 3642)
        etg1(E(True), 24.5, 42.2, 3616)
    else:
        etg2(E(False), 11.9, 9.8, 11.6, 16.2, 5.6, 15.4)
        etg2(E(True), 11.8, 7.8, 11.9, 16.3, 5.4, 15.3)
    r(M - IV, 0, IV + IV, D, MORK)                          # leilighetsskille
    sone(1500, -900, sone_tekst)
    skriv(navn, viewbox, tittel)


bygg("1. etasje", "-2500 -1700 20300 24800", (-2300, 21600),
     "1. ETASJE · TO ENHETER")
bygg("2. etasje", "-2500 -1700 20300 21200", (-2300, 18400),
     "2. ETASJE · TO ENHETER")
