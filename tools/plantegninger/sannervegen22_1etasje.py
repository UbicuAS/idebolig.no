# -*- coding: utf-8 -*-
"""Stilprøve: møblert 2D-plantegning av 1. etasje, Sannervegen 22 (prosjekt 1211).
Geometri i mm fra E-3 Plan 1. etasje (17.08.2026). Genererer SVG."""

UT = r"C:\Users\mresv\AppData\Local\Temp\claude\Z--nettside-Roar\25778229-9385-48c2-8d63-b3c7e667ecd5\scratchpad\sannervegen22-1etasje.svg"

# Farger (Idébolig-katalogens palett)
MORK = "#33302C"; GRAA = "#6b6257"; GULL = "#C99C55"
PARKETT = "#EAD9BC"; PARKETT_L = "#D9C4A3"
FLIS = "#E9EAE7"; FLIS_L = "#D2D6D2"
DEKKE = "#D4C9B8"; DEKKE_L = "#C2B5A0"
MOEBEL = "#FBF8F2"; MOEBEL_K = "#8C8378"

YV = 200   # yttervegg
IV = 100   # innervegg

deler = []


def r(x, y, w, h, fill, stroke="none", sw=0, rx=0, o=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    deler.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{sw}" rx="{rx}" opacity="{o}"{d}/>')


def linje(x1, y1, x2, y2, stroke, sw, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    deler.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
                 f'stroke-width="{sw}"{d}/>')


def tekst(x, y, s, storrelse, farge=MORK, vekt=600, anker="middle"):
    deler.append(f'<text x="{x}" y="{y}" font-size="{storrelse}" fill="{farge}" '
                 f'font-weight="{vekt}" text-anchor="{anker}" '
                 f'font-family="Poppins, Segoe UI, sans-serif">{s}</text>')


def romnavn(x, y, navn, areal):
    tekst(x, y, navn, 320, MORK, 600)
    tekst(x, y + 360, f"{areal} m²", 240, GRAA, 400)


def vindu(x, y, lengde, retning):
    if retning == "h":
        r(x, y, lengde, YV, "#FDFBF7")
        linje(x, y + 30, x + lengde, y + 30, MORK, 26)
        linje(x, y + YV - 30, x + lengde, y + YV - 30, MORK, 26)
        linje(x, y + YV / 2, x + lengde, y + YV / 2, MORK, 20)
        linje(x, y, x, y + YV, MORK, 26); linje(x + lengde, y, x + lengde, y + YV, MORK, 26)
    else:
        r(x, y, YV, lengde, "#FDFBF7")
        linje(x + 30, y, x + 30, y + lengde, MORK, 26)
        linje(x + YV - 30, y, x + YV - 30, y + lengde, MORK, 26)
        linje(x + YV / 2, y, x + YV / 2, y + lengde, MORK, 20)
        linje(x, y, x + YV, y, MORK, 26); linje(x, y + lengde, x + YV, y + lengde, MORK, 26)


def door(x, y, bredde, veggT, retning, hengsel="start", sving="inn", gulv="#FDFBF7"):
    """Dør: gap i vegg + dørblad + slagbue.
    retning h = veggen ligger horisontalt. sving inn = mot økende koordinat."""
    if retning == "h":
        r(x, y, bredde, veggT, gulv)
        hx = x if hengsel == "start" else x + bredde
        s = 1 if hengsel == "start" else -1
        vy = y + (veggT if sving == "inn" else 0)
        ey = vy + (bredde if sving == "inn" else -bredde)
        deler.append(f'<path d="M {hx} {vy} L {hx} {ey}" stroke="{MORK}" stroke-width="30" fill="none"/>')
        deler.append(f'<path d="M {hx + s * bredde} {vy} A {bredde} {bredde} 0 0 '
                     f'{1 if (hengsel == "start") == (sving == "inn") else 0} {hx} {ey}" '
                     f'stroke="{MOEBEL_K}" stroke-width="16" fill="none" stroke-dasharray="70 70"/>')
    else:
        r(x, y, veggT, bredde, gulv)
        hy = y if hengsel == "start" else y + bredde
        s = 1 if hengsel == "start" else -1
        vx = x + (veggT if sving == "inn" else 0)
        ex = vx + (bredde if sving == "inn" else -bredde)
        deler.append(f'<path d="M {vx} {hy} L {ex} {hy}" stroke="{MORK}" stroke-width="30" fill="none"/>')
        deler.append(f'<path d="M {vx} {hy + s * bredde} A {bredde} {bredde} 0 0 '
                     f'{0 if (hengsel == "start") == (sving == "inn") else 1} {ex} {hy}" '
                     f'stroke="{MOEBEL_K}" stroke-width="16" fill="none" stroke-dasharray="70 70"/>')


def mobel_rect(x, y, w, h, rx=40, fyll=MOEBEL, kant=MOEBEL_K, sw=22):
    r(x, y, w, h, fyll, kant, sw, rx=rx)


def seng(x, y, w, h):
    """Seng med hodegjerde øverst, puter og dyne."""
    mobel_rect(x, y, w, h, rx=60)
    linje(x, y + 140, x + w, y + 140, MOEBEL_K, 20)
    if w > 1400:
        pw = (w - 240) / 2
        r(x + 80, y + 220, pw, 340, "#F3EDE2", MOEBEL_K, 18, rx=70)
        r(x + 160 + pw, y + 220, pw, 340, "#F3EDE2", MOEBEL_K, 18, rx=70)
    else:
        r(x + 80, y + 220, w - 160, 340, "#F3EDE2", MOEBEL_K, 18, rx=70)
    r(x + 60, y + 680, w - 120, h - 760, "#F6F1E7", MOEBEL_K, 18, rx=50)
    linje(x + 60, y + 820, x + w - 60, y + 820, MOEBEL_K, 14)


def nattbord(x, y, s=420):
    mobel_rect(x, y, s, s, rx=40)


def garderobe(x, y, w, h):
    """Garderobeskap: ramme + skyvedørslinje + heng."""
    mobel_rect(x, y, w, h, rx=20)
    if w >= h:
        linje(x + 60, y + h / 2, x + w - 60, y + h / 2, MOEBEL_K, 16, dash="180 90")
        linje(x + w / 2, y, x + w / 2, y + h, MOEBEL_K, 16)
    else:
        linje(x + w / 2, y + 60, x + w / 2, y + h - 60, MOEBEL_K, 16, dash="180 90")
        linje(x, y + h / 2, x + w, y + h / 2, MOEBEL_K, 16)


def sofa(x, y, w, h):
    """Sofa med rygg mot sør (nederst) og armlener."""
    mobel_rect(x, y, w, h, rx=90)
    r(x + 40, y + h - 260, w - 80, 220, "#F3EDE2", MOEBEL_K, 16, rx=90)
    r(x + 40, y + 40, 220, h - 80, "#F3EDE2", MOEBEL_K, 16, rx=90)
    r(x + w - 260, y + 40, 220, h - 80, "#F3EDE2", MOEBEL_K, 16, rx=90)
    n = max(2, int((w - 520) // 850))
    for i in range(1, n):
        linje(x + 260 + i * (w - 520) / n, y + 60, x + 260 + i * (w - 520) / n, y + h - 280, MOEBEL_K, 14)


def bord(x, y, w, h, rx=60, fyll="#F3EAD9"):
    mobel_rect(x, y, w, h, rx=rx, fyll=fyll)


def stol(x, y, s=420):
    mobel_rect(x, y, s, s, rx=110)


def vask(cx, cy, rr=170):
    deler.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="#F6F3EC" stroke="{MOEBEL_K}" stroke-width="20"/>')
    deler.append(f'<circle cx="{cx}" cy="{cy}" r="{int(rr*0.45)}" fill="none" stroke="{MOEBEL_K}" stroke-width="14"/>')


def komfyr(x, y, s=520):
    mobel_rect(x, y, s, s, rx=30)
    for dx, dy in ((0.3, 0.3), (0.7, 0.3), (0.3, 0.7), (0.7, 0.7)):
        deler.append(f'<circle cx="{x + s * dx}" cy="{y + s * dy}" r="{s * 0.13}" '
                     f'fill="none" stroke="{MOEBEL_K}" stroke-width="18"/>')


def toalett(x, y, retn="n"):
    """Toalett; retn = veggen sisterna står mot."""
    if retn == "n":
        r(x, y, 420, 200, MOEBEL, MOEBEL_K, 20, rx=40)
        deler.append(f'<ellipse cx="{x + 210}" cy="{y + 470}" rx="185" ry="255" '
                     f'fill="{MOEBEL}" stroke="{MOEBEL_K}" stroke-width="20"/>')
    elif retn == "s":
        r(x, y + 480, 420, 200, MOEBEL, MOEBEL_K, 20, rx=40)
        deler.append(f'<ellipse cx="{x + 210}" cy="{y + 210}" rx="185" ry="255" '
                     f'fill="{MOEBEL}" stroke="{MOEBEL_K}" stroke-width="20"/>')


def badekar(x, y, w=1700, h=750):
    mobel_rect(x, y, w, h, rx=60)
    r(x + 90, y + 90, w - 180, h - 180, "#F1EFE9", MOEBEL_K, 16, rx=200)


def vaskemaskin(x, y, s=600):
    mobel_rect(x, y, s, s, rx=30)
    deler.append(f'<circle cx="{x + s/2}" cy="{y + s/2}" r="{s*0.3}" fill="none" stroke="{MOEBEL_K}" stroke-width="18"/>')


def teppe(x, y, w, h):
    r(x, y, w, h, "#E4D2AE", "#CDB588", 22, rx=120, o=0.85)


def trapp(x, y, w, h, opp="n", trinn=9):
    r(x, y, w, h, "#F6F2EA", MOEBEL_K, 22)
    for i in range(1, trinn):
        linje(x, y + i * h / trinn, x + w, y + i * h / trinn, MOEBEL_K, 16)
    ax = x + w / 2
    y1, y2 = (y + h - 200, y + 260) if opp == "n" else (y + 200, y + h - 260)
    deler.append(f'<line x1="{ax}" y1="{y1}" x2="{ax}" y2="{y2}" stroke="{GRAA}" stroke-width="34"/>')
    pil = -1 if opp == "n" else 1
    deler.append(f'<path d="M {ax - 130} {y2 - pil * 200} L {ax} {y2} L {ax + 130} {y2 - pil * 200}" '
                 f'fill="none" stroke="{GRAA}" stroke-width="34"/>')


# ---------------------------------------------------------------- geometri
# Sone A (lukket): x 0-7900, y 1100-3600.  Sone B: x 0-12670, y 3600-11320.
# Takoverbygg (åpent, under tak): x 7900-12670, y 1100-3600.

svg_hode = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="-600 -1450 13900 14700"
     font-family="Poppins, Segoe UI, sans-serif">
<defs>
  <pattern id="parkett" width="1200" height="360" patternUnits="userSpaceOnUse">
    <rect width="1200" height="360" fill="{PARKETT}"/>
    <line x1="0" y1="120" x2="1200" y2="120" stroke="{PARKETT_L}" stroke-width="16"/>
    <line x1="0" y1="240" x2="1200" y2="240" stroke="{PARKETT_L}" stroke-width="16"/>
    <line x1="0" y1="360" x2="1200" y2="360" stroke="{PARKETT_L}" stroke-width="16"/>
    <line x1="300" y1="0" x2="300" y2="120" stroke="{PARKETT_L}" stroke-width="16"/>
    <line x1="900" y1="120" x2="900" y2="240" stroke="{PARKETT_L}" stroke-width="16"/>
    <line x1="600" y1="240" x2="600" y2="360" stroke="{PARKETT_L}" stroke-width="16"/>
  </pattern>
  <pattern id="flis" width="300" height="300" patternUnits="userSpaceOnUse">
    <rect width="300" height="300" fill="{FLIS}"/>
    <path d="M 300 0 L 0 0 0 300" fill="none" stroke="{FLIS_L}" stroke-width="14"/>
  </pattern>
  <pattern id="dekke" width="1600" height="290" patternUnits="userSpaceOnUse">
    <rect width="1600" height="290" fill="{DEKKE}"/>
    <line x1="0" y1="145" x2="1600" y2="145" stroke="{DEKKE_L}" stroke-width="18"/>
    <line x1="0" y1="290" x2="1600" y2="290" stroke="{DEKKE_L}" stroke-width="18"/>
    <line x1="500" y1="0" x2="500" y2="145" stroke="{DEKKE_L}" stroke-width="18"/>
    <line x1="1100" y1="145" x2="1100" y2="290" stroke="{DEKKE_L}" stroke-width="18"/>
  </pattern>
  <filter id="skygge" x="-8%" y="-8%" width="116%" height="116%">
    <feDropShadow dx="0" dy="90" stdDeviation="140" flood-color="#33302C" flood-opacity="0.22"/>
  </filter>
</defs>
""".replace("{PARKETT}", PARKETT).replace("{PARKETT_L}", PARKETT_L) \
   .replace("{FLIS}", FLIS).replace("{FLIS_L}", FLIS_L) \
   .replace("{DEKKE}", DEKKE).replace("{DEKKE_L}", DEKKE_L)

# --- bygningsskygge (samlet fotavtrykk)
deler.append('<path d="M 0 1100 H 12670 V 11320 H 0 Z" fill="#FDFBF7" filter="url(#skygge)"/>')

# --- gulv
r(0, 1100, 7900, 2500, "url(#parkett)")          # sone A grunnflate
r(0, 3600, 12670, 7720, "url(#parkett)")         # sone B grunnflate
r(0, 1100, 3700, 2500, "url(#flis)")             # bad
r(3700, 1100, 1200, 1300, "url(#flis)")          # wc
r(7900, 1100, 4770, 2500, "url(#dekke)")         # takoverbygg (ute, under tak)
r(9270, 11320, 3400, 1750, "url(#dekke)")        # terrasse ved stuedør (ute)

# --- takoverbygg: stiplet takkant
deler.append(f'<rect x="7900" y="1100" width="4770" height="2500" fill="none" '
             f'stroke="{GRAA}" stroke-width="26" stroke-dasharray="240 140"/>')

# --- utvendig trapp ned til inngang (nord)
trapp(3700, -60, 1700, 1160, opp="s", trinn=7)

# --- yttervegger
r(0, 1100, 3700 + IV, YV, MORK)                 # nord: bad + wc
r(3800, 1100, 1700, YV, MORK)                   # nord: landing (m/ inngangsdør)
r(5500 - IV, 1100, 2400 + IV + YV, YV, MORK)    # nord: gang-tilbygg
r(0, 1100, YV, 2500, MORK)                      # vest, sone A
r(0, 3600, YV, 7720, MORK)                      # vest, sone B
r(0, 11320 - YV, 12670, YV, MORK)               # sør
r(12670 - YV, 3600, YV, 7720, MORK)             # øst, sone B
r(7900 - YV, 1100, YV, 2500 + IV, MORK)         # øst, sone A (mot takoverbygg)
r(0, 3600 - IV, 7900, IV + IV, MORK)            # skille sone A/B
r(7900 - YV, 3600 - IV, 4770 + YV, IV + IV, MORK)  # nordvegg sone B mot takoverbygg

# --- innervegger
r(3700, 1100, IV, 2500, MORK)                   # bad | landing
r(3700, 2400, 1200, IV, MORK)                   # wc sør
r(4800, 1100, IV, 1300 + IV, MORK)              # wc øst
r(5500 - IV, 1100, IV, 2500, MORK)              # landing | gang
r(3000, 3600, IV, 7720, MORK)                   # sov-vegg mot entré/stue (hele)
r(0, 7700, 3000 + IV, IV, MORK)                 # sov12 | sov10
r(3000, 7220, 4900, IV, MORK)                   # entré | stue
r(7900 - IV, 3600, IV, 1900, MORK)              # trappevange mot øst-fløy

# --- vinduer
vindu(0, 4600, 1600, "v")                       # sov12 vest 1.60x1.20
vindu(0, 8900, 1200, "v")                       # sov10 vest 1.20x1.20
vindu(1500, 11320 - YV, 1150, "h")              # sov10 sør 1.15x1.40
vindu(4300, 11320 - YV, 1150, "h")              # stue sør 1.15x1.40
vindu(6600, 11320 - YV, 1150, "h")              # stue sør 1.15x1.40
vindu(10400, 11320 - YV, 2200, "h")             # stue sør 2.20x1.60
vindu(12670 - YV, 4400, 1400, "v")              # stue øst 1.40x1.20
vindu(12670 - YV, 6600, 1400, "v")              # stue øst 1.40x1.20
vindu(800, 1100, 800, "h")                      # bad nord 0.80x0.60

# --- dører
door(4400, 1100, 890, YV, "h", "start", "inn")                       # inngangsdør -> landing
door(7900 - YV, 1900, 890, YV, "v", "start", "inn", gulv=PARKETT)    # takoverbygg -> gang
door(5500 - IV, 2200, 890, IV, "v", "end", "inn", gulv=PARKETT)      # landing <-> gang
door(3700, 2500, 790, IV, "v", "start", "ut", gulv=FLIS)             # bad (slår inn i badet)
door(4000, 2400, 690, IV, "h", "start", "inn", gulv=FLIS)            # wc (slår inn i wc? nei, ut i landing)
door(3000, 6100, 890, IV, "v", "end", "ut", gulv=PARKETT)            # sov12 (slår inn i rommet)
r(3800, 3600 - IV, 1600, IV + IV, "url(#parkett)")                   # åpen passasje inngang->entré
door(3000, 8000, 890, IV, "v", "start", "ut", gulv=PARKETT)          # sov10 (slår inn i rommet)
door(9100, 11320 - YV, 900, YV, "h", "start", "inn", gulv=PARKETT)   # terrassedør (NED ute)
r(5300, 7220, 1500, IV, "url(#parkett)")                             # åpen passasje entré->stue

# --- innvendig trapp (entré)
trapp(6350, 3750, 1450, 1750, opp="n", trinn=9)
tekst(7075, 5780, "OPP/NED", 170, GRAA, 500)

# --- BAD: kar, servantskap m/ 2 vasker, vaskemaskin, toalett mot sør
badekar(300, 1420)
bord(2150, 1380, 1400, 540, rx=20, fyll=MOEBEL)
vask(2520, 1650); vask(3170, 1650)
vaskemaskin(300, 2850)
toalett(2650, 2850, "s")
# --- WC
toalett(3800, 1180, "n")
# --- GANG (inngangsparti i tilbygget)
garderobe(6950, 1250, 750, 620)
mobel_rect(5650, 3080, 1200, 400)               # benk
teppe(5750, 1500, 800, 1300)
# --- SOV 12
seng(650, 3800, 1800, 2100)
nattbord(200, 3830); nattbord(2480, 3830)
garderobe(300, 7060, 1600, 550)
# --- SOV 10
seng(550, 7800, 1600, 2000)
garderobe(2380, 9300, 550, 1650)
# --- ENTRÉ
mobel_rect(3150, 5300, 450, 1500)               # konsollbord langs veggen
teppe(4200, 4600, 1100, 1800)
# --- STUE: kjøkken i øst-fløyen
bord(8700, 3800, 700, 700, rx=30, fyll=MOEBEL)  # kjøl
mobel_rect(9400, 3800, 2670, 400, rx=20)        # benk nord
mobel_rect(12070, 3800, 400, 2600, rx=20)       # benk øst
komfyr(9700, 3820, 460)
vask(12270, 4600, 160)
bord(9300, 5300, 2200, 1000, rx=80)             # spisebord
for sx in (9500, 10300, 11100):
    stol(sx, 4820); stol(sx, 6340)
# --- STUE: sofagruppe
teppe(3900, 8300, 3300, 2300)
sofa(3950, 9700, 2900, 1050)
bord(4900, 8750, 1150, 650, rx=200)
mobel_rect(6950, 7450, 1800, 420)               # tv-benk mot entrévegg
# --- TAKOVERBYGG: utemøbler
bord(9750, 2000, 900, 900, rx=450)
stol(9250, 2230); stol(10800, 2230)
# --- TERRASSE SØR: nedgang
deler.append(f'<path d="M 10600 12300 L 10150 12300" stroke="{GRAA}" stroke-width="30"/>')
deler.append(f'<path d="M 10330 12150 L 10150 12300 L 10330 12450" fill="none" stroke="{GRAA}" stroke-width="30"/>')
tekst(10950, 12400, "NED", 190, GRAA, 500)

# --- romnavn
romnavn(1850, 2550, "Bad", 9)
tekst(4200, 2150, "WC", 200, MORK, 600)
romnavn(6650, 2600, "Gang", 5)
romnavn(10300, 1750, "Takoverbygg", 18)
romnavn(1550, 6650, "Sov", 12)
romnavn(1450, 10550, "Sov", 10)
romnavn(4700, 4150, "Entré", 19)
romnavn(8000, 9600, "Stue", 46)
tekst(10950, 11980, "Terrasse", 220, GRAA, 500)

# --- tittellinje
tekst(60, 12780, "Sannervegen 22 — 1. etasje", 340, MORK, 600, anker="start")
tekst(60, 13160, "Møblert plantegning · møblering er illustrativ", 220, GRAA, 400, anker="start")

svg = svg_hode + "\n".join(deler) + "\n</svg>\n"
with open(UT, "w", encoding="utf-8") as f:
    f.write(svg)
print("skrev", UT, len(svg), "tegn")
