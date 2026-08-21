# -*- coding: utf-8 -*-
"""Møblerte 2D-plantegninger for Edvard Prakt (katalogmodell) — tre etasjer,
tegnet fra CAD-skjermbildene Marius sendte 21.08.2026.
U.etg 17000x8500 (utleiedel 47 m² + kjeller 64 m²), 1.etg 84 m² + garasje
36,6 m² + terrasse 22,5 m², 2.etg 84 m² + takterrasse 42,7 m²."""
import os

MAPPE = r"C:\Users\mresv\AppData\Local\Temp\claude\Z--nettside-Roar\25778229-9385-48c2-8d63-b3c7e667ecd5\scratchpad"

MORK = "#33302C"; GRAA = "#6b6257"; GULL = "#C99C55"
PARKETT = "#EAD9BC"; PARKETT_L = "#D9C4A3"
FLIS = "#E9EAE7"; FLIS_L = "#D2D6D2"
DEKKE = "#D4C9B8"; DEKKE_L = "#C2B5A0"
BETONG = "#DDDAD3"; BETONG_L = "#CBC7BD"
MOEBEL = "#FBF8F2"; MOEBEL_K = "#8C8378"

YV = 250   # yttervegg (250 i grunnlaget)
IV = 100

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


def romnavn(x, y, navn, areal=None, s1=320, s2=240):
    tekst(x, y, navn, s1, MORK, 600)
    if areal is not None:
        tekst(x, y + s1 + 40, f"{areal} m²", s2, GRAA, 400)


def sone(x, y, s):
    tekst(x, y, s, 230, GULL, 600)


def vindu(x, y, lengde, retning, t=YV):
    if retning == "h":
        r(x, y, lengde, t, "#FDFBF7")
        linje(x, y + 34, x + lengde, y + 34, MORK, 28)
        linje(x, y + t - 34, x + lengde, y + t - 34, MORK, 28)
        linje(x, y + t / 2, x + lengde, y + t / 2, MORK, 20)
        linje(x, y, x, y + t, MORK, 28); linje(x + lengde, y, x + lengde, y + t, MORK, 28)
    else:
        r(x, y, t, lengde, "#FDFBF7")
        linje(x + 34, y, x + 34, y + lengde, MORK, 28)
        linje(x + t - 34, y, x + t - 34, y + lengde, MORK, 28)
        linje(x + t / 2, y, x + t / 2, y + lengde, MORK, 20)
        linje(x, y, x + t, y, MORK, 28); linje(x, y + lengde, x + t, y + lengde, MORK, 28)


def door(x, y, bredde, veggT, retning, hengsel="start", sving="inn", gulv="#FDFBF7"):
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
    mobel_rect(x, y, w, h, rx=20)
    if w >= h:
        linje(x + 60, y + h / 2, x + w - 60, y + h / 2, MOEBEL_K, 16, dash="180 90")
        linje(x + w / 2, y, x + w / 2, y + h, MOEBEL_K, 16)
    else:
        linje(x + w / 2, y + 60, x + w / 2, y + h - 60, MOEBEL_K, 16, dash="180 90")
        linje(x, y + h / 2, x + w, y + h / 2, MOEBEL_K, 16)


def sofa(x, y, w, h, rygg="s"):
    """Rygg mot s (nederst) eller n (øverst)."""
    mobel_rect(x, y, w, h, rx=90)
    ry = y + h - 260 if rygg == "s" else y + 40
    r(x + 40, ry, w - 80, 220, "#F3EDE2", MOEBEL_K, 16, rx=90)
    r(x + 40, y + 40, 220, h - 80, "#F3EDE2", MOEBEL_K, 16, rx=90)
    r(x + w - 260, y + 40, 220, h - 80, "#F3EDE2", MOEBEL_K, 16, rx=90)
    n = max(2, int((w - 520) // 850))
    y1 = y + (280 if rygg == "n" else 60)
    y2 = y + h - (60 if rygg == "n" else 280)
    for i in range(1, n):
        linje(x + 260 + i * (w - 520) / n, y1, x + 260 + i * (w - 520) / n, y2, MOEBEL_K, 14)


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
    if retn == "n":
        r(x, y, 420, 200, MOEBEL, MOEBEL_K, 20, rx=40)
        deler.append(f'<ellipse cx="{x + 210}" cy="{y + 470}" rx="185" ry="255" '
                     f'fill="{MOEBEL}" stroke="{MOEBEL_K}" stroke-width="20"/>')
    elif retn == "s":
        r(x, y + 480, 420, 200, MOEBEL, MOEBEL_K, 20, rx=40)
        deler.append(f'<ellipse cx="{x + 210}" cy="{y + 210}" rx="185" ry="255" '
                     f'fill="{MOEBEL}" stroke="{MOEBEL_K}" stroke-width="20"/>')


def dusj(x, y, s=900):
    mobel_rect(x, y, s, s, rx=30, fyll="#F1EFE9")
    deler.append(f'<circle cx="{x + s/2}" cy="{y + s/2}" r="90" fill="none" stroke="{MOEBEL_K}" stroke-width="16"/>')
    linje(x + 60, y + 60, x + s - 60, y + s - 60, MOEBEL_K, 12)
    linje(x + s - 60, y + 60, x + 60, y + s - 60, MOEBEL_K, 12)


def badekar(x, y, w=1700, h=750):
    mobel_rect(x, y, w, h, rx=60)
    r(x + 90, y + 90, w - 180, h - 180, "#F1EFE9", MOEBEL_K, 16, rx=200)


def vaskemaskin(x, y, s=600, tt="V"):
    mobel_rect(x, y, s, s, rx=30)
    deler.append(f'<circle cx="{x + s/2}" cy="{y + s/2}" r="{s*0.3}" fill="none" stroke="{MOEBEL_K}" stroke-width="18"/>')


def teppe(x, y, w, h):
    r(x, y, w, h, "#E4D2AE", "#CDB588", 22, rx=120, o=0.85)


def trapp(x, y, w, h, opp="n", trinn=9, tekst_under=True):
    r(x, y, w, h, "#F6F2EA", MOEBEL_K, 22)
    for i in range(1, trinn):
        linje(x, y + i * h / trinn, x + w, y + i * h / trinn, MOEBEL_K, 16)
    ax = x + w / 2
    y1, y2 = (y + h - 200, y + 260) if opp == "n" else (y + 200, y + h - 260)
    deler.append(f'<line x1="{ax}" y1="{y1}" x2="{ax}" y2="{y2}" stroke="{GRAA}" stroke-width="34"/>')
    pil = -1 if opp == "n" else 1
    deler.append(f'<path d="M {ax - 130} {y2 - pil * 200} L {ax} {y2} L {ax + 130} {y2 - pil * 200}" '
                 f'fill="none" stroke="{GRAA}" stroke-width="34"/>')
    if tekst_under:
        tekst(ax, y + h + 300, "OPP/NED", 170, GRAA, 500)


def hylle(x, y, w, h):
    """Enkel hylle/benk med langsgående delelinje."""
    mobel_rect(x, y, w, h, rx=20)
    if w >= h:
        linje(x + 40, y + h / 2, x + w - 40, y + h / 2, MOEBEL_K, 14)
    else:
        linje(x + w / 2, y + 40, x + w / 2, y + h - 40, MOEBEL_K, 14)


HODE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}"
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
  <pattern id="betong" width="900" height="900" patternUnits="userSpaceOnUse">
    <rect width="900" height="900" fill="{BETONG}"/>
    <circle cx="200" cy="260" r="26" fill="{BETONG_L}"/>
    <circle cx="640" cy="150" r="20" fill="{BETONG_L}"/>
    <circle cx="470" cy="560" r="30" fill="{BETONG_L}"/>
    <circle cx="760" cy="740" r="22" fill="{BETONG_L}"/>
    <circle cx="130" cy="760" r="18" fill="{BETONG_L}"/>
  </pattern>
  <filter id="skygge" x="-8%" y="-8%" width="116%" height="116%">
    <feDropShadow dx="0" dy="90" stdDeviation="140" flood-color="#33302C" flood-opacity="0.22"/>
  </filter>
</defs>
""".replace("{PARKETT}", PARKETT).replace("{PARKETT_L}", PARKETT_L) \
   .replace("{FLIS}", FLIS).replace("{FLIS_L}", FLIS_L) \
   .replace("{DEKKE}", DEKKE).replace("{DEKKE_L}", DEKKE_L) \
   .replace("{BETONG}", BETONG).replace("{BETONG_L}", BETONG_L)


def skriv(navn, viewbox, tittel):
    global deler
    tx, ty = tittel
    tekst(tx, ty, f"Edvard Prakt — {navn}", 380, MORK, 600, anker="start")
    fil = os.path.join(MAPPE, f"edvard-prakt-{navn.replace('. ', '').replace(' ', '-').lower()}.svg")
    svg = HODE.replace("{VB}", viewbox) + "\n".join(deler) + "\n</svg>\n"
    with open(fil, "w", encoding="utf-8") as f:
        f.write(svg)
    print("skrev", fil, len(svg))
    deler = []


# ================================================================ U. ETASJE
# 17000 x 8500. Utleiedel (47 m²) = øvre bånd av venstre blokk (0-11000).
# Kjeller (64 m²) = nedre bånd + høyre blokk (11000-17000, fra y=1500).
def uetg():
    deler.append('<path d="M 0 0 H 11000 V 1500 H 17000 V 8500 H 0 Z" '
                 'fill="#FDFBF7" filter="url(#skygge)"/>')
    # gulv
    r(0, 0, 11000, 8500, "url(#parkett)")
    r(11000, 1500, 6000, 7000, "url(#parkett)")
    r(3300, 0, 1800, 3500, "url(#flis)")                    # bad
    r(0, 4700, 3000, 3800, "url(#parkett)")                 # teknisk/vask (parkett iht. brief)
    # lyssjakt mellom blokkene
    r(11000, 1500, 1300, 1300, "#F1ECE1", GRAA, 22, dash="140 90")
    tekst(11650, 2250, "Sjakt", 170, GRAA, 500)

    # yttervegger
    r(0, 0, 11000 + YV, YV, MORK)                           # nord venstre blokk
    r(11000, 1500, 6000, YV, MORK)                          # nord høyre blokk
    r(0, 0, YV, 8500, MORK)                                 # vest
    r(0, 8500 - YV, 17000, YV, MORK)                        # sør
    r(17000 - YV, 1500, YV, 7000, MORK)                     # øst
    r(11000, 0, YV, 1500 + YV, MORK)                        # øst venstre blokk (mot sjakt)

    # innervegger — utleiedel
    r(3300, 0, IV, 3500, MORK)                              # sov | bad
    r(5100, 0, IV, 3500, MORK)                              # bad | stue
    r(0, 3500, 5200, IV, MORK)                              # sov/bad sør (mot gang)
    r(9300, 0, IV, 3900, MORK)                              # stue | bod 3.3
    r(9300, 3900, 1700, IV, MORK)                           # bod 3.3 sør
    r(0, 4300, 3000, IV, MORK)                              # gang sør / teknisk nord (vest)
    r(3000, 4300, IV, 4200, MORK)                           # teknisk øst
    r(3000, 4600, 8000 + IV, IV, MORK)                      # skille utleiedel/kjellergang
    # innervegger — kjeller
    r(7800, 4700, IV, 2500, MORK)                           # trapperom øst
    r(7900, 6300, 1500, IV, MORK)                           # bod 3.8 sør
    r(9400, 4700, IV, 1700, MORK)                           # bod 3.8 øst
    r(11000, 1500, IV, 5000, MORK)                          # kjellerstue vest (m/ åpning)
    r(13700, 6300, 3300, IV, MORK)                          # disp nord
    r(13700, 6300, IV, 2200, MORK)                          # disp vest

    # vinduer
    vindu(900, 0, 1500, "h")                                # sov nord
    vindu(0, 900, 1200, "v")                                # sov vest
    vindu(6200, 0, 1300, "h")                               # stue nord
    vindu(8000, 0, 900, "h")                                # stue nord 2
    vindu(13200, 1500, 1400, "h")                           # kjellerstue nord
    vindu(17000 - YV, 3300, 1400, "v")                      # kjellerstue øst
    vindu(1200, 8500 - YV, 900, "h")                        # teknisk sør

    # dører
    door(5600, 8500 - YV, 900, YV, "h", "start", "ut")                    # inngang kjeller (sør)
    door(3300, 3500, 800, IV, "v", "start", "ut", gulv=FLIS) if False else None
    door(3450, 3500, 800, IV, "h", "start", "ut", gulv=FLIS)              # bad (fra gang)
    door(700, 3500, 890, IV, "h", "end", "ut", gulv=PARKETT)              # sov (fra gang)
    door(5700, 3500, 0, IV, "h") if False else None
    r(5200, 3500, 900, IV, "url(#parkett)")                               # åpning gang->stue
    door(9300, 2900, 800, IV, "v", "end", "ut", gulv=PARKETT)             # bod 3.3
    door(4100, 4600, 900, IV + IV, "h", "start", "inn", gulv=PARKETT)     # utleiedel <-> kjellergang
    door(3000, 5300, 890, IV, "v", "start", "inn", gulv=PARKETT)          # teknisk/vask
    door(8300, 6300, 800, IV, "h", "start", "ut", gulv=PARKETT)           # bod 3.8
    r(11000, 4400, IV, 1100, "url(#parkett)")                             # åpning -> kjellerstue
    door(13700, 6800, 890, IV, "v", "start", "inn", gulv=PARKETT)         # disp

    # trapp (gjennomgående)
    trapp(6000, 4700, 1800, 2500, opp="n", trinn=10)

    # møblering — utleiedel
    seng(700, 700, 1800, 2100)
    nattbord(300, 730); nattbord(2550, 730)
    garderobe(400, 2900, 1900, 550)
    dusj(3450, 250, 850)
    vask(4700, 700, 160)
    toalett(4450, 2850, "s")
    vaskemaskin(3450, 1350)
    hylle(5250, 250, 550, 2200)                            # kjøkkenrekke (utleiedel)
    komfyr(5270, 900, 500)
    vask(5520, 2000, 150)
    sofa(6600, 300, 2300, 950, rygg="n")
    bord(7200, 1500, 1000, 600, rx=150)
    teppe(6500, 1350, 2400, 900)
    hylle(6300, 3050, 1800, 400)                           # tv-benk mot gangvegg
    # møblering — kjeller
    vaskemaskin(350, 5000); vaskemaskin(1000, 5000)
    hylle(350, 7700, 2300, 500)
    hylle(8000, 4800, 500, 1400)                           # bodhylle
    sofa(13600, 2300, 2700, 1000, rygg="n")
    bord(14400, 3900, 1100, 650, rx=200)
    teppe(13900, 3600, 2300, 1300)
    hylle(11400, 5700, 1600, 420)                          # tv-benk kjellerstue
    hylle(14000, 6700, 500, 1400)                          # disp-hylle

    # romnavn
    romnavn(1650, 1900, "Sov", 12)
    romnavn(4200, 1800, "Bad", 6.3)
    romnavn(7600, 2350, "Stue", 16.6)
    tekst(10150, 1900, "Bod", 210, MORK, 600); tekst(10150, 2150, "3,3 m²", 170, GRAA, 400)
    romnavn(2600, 4150, "Gang", 6, s1=250, s2=190) if False else tekst(2300, 4100, "Gang 6 m²", 210, GRAA, 500)
    romnavn(1500, 6300, "Teknisk/Vask", 10.8, s1=270, s2=210)
    tekst(8650, 5300, "Bod", 210, MORK, 600); tekst(8650, 5550, "3,8 m²", 170, GRAA, 400)
    romnavn(14300, 4900, "Kjellerstue", 24.5)
    romnavn(15300, 7300, "Disp.", 6.7, s1=270, s2=210)
    sone(1900, -350, "UTLEIEDEL · BRA 47 M²")
    sone(14000, 9000, "KJELLER · BRA 64 M²")

    skriv("U. etasje", "-700 -1100 18500 11400", (-500, 9800))


# ================================================================ 1. ETASJE
# Hovedblokk 11000x8500, garasje 11000-17000 (y 1200-7300),
# terrasse vest 2700 bred, inngang nord + bislag sør.
def etg1():
    deler.append('<path d="M 0 0 H 11000 V 1200 H 17000 V 7300 H 11000 V 8500 H 0 Z" '
                 'fill="#FDFBF7" filter="url(#skygge)"/>')
    # utedekker
    r(-2700, 0, 2700, 8500, "url(#dekke)")
    deler.append(f'<rect x="-2700" y="0" width="2700" height="8500" fill="none" '
                 f'stroke="{GRAA}" stroke-width="26" stroke-dasharray="240 140"/>')
    r(4300, -1350, 2400, 1350, "url(#dekke)")               # inngangsrepos nord
    r(4000, 8500, 2000, 1200, "url(#dekke)")                # bislag sør
    # gulv
    r(0, 0, 11000, 8500, "url(#parkett)")
    r(11000, 1200, 6000, 6100, "url(#betong)")              # garasje
    r(9000, 4600, 2000, 2700, "url(#flis)")                 # wc
    # yttervegger
    r(0, 0, 11000, YV, MORK)                                # nord
    r(0, 0, YV, 8500, MORK)                                 # vest
    r(0, 8500 - YV, 11000, YV, MORK)                        # sør
    r(11000 - YV, 0, YV, 8500, MORK)                        # øst (hus)
    r(11000, 1200, 6000, YV, MORK)                          # garasje nord
    r(11000, 7300 - YV, 6000, YV, MORK)                     # garasje sør
    r(17000 - YV, 1200, YV, 6100, MORK)                     # garasje øst
    # innervegger
    r(0, 4600, 4000 + IV, IV, MORK)                         # sov nord
    r(4000, 4600, IV, 3900, MORK)                           # sov øst
    r(7300, 4600, 3700, IV, MORK)                           # vf/wc nord (mot stue)
    r(9000, 4600, IV, 2700, MORK)                           # wc vest
    r(9000, 7300, 2000, IV, MORK)                           # wc sør
    # vinduer
    vindu(700, 0, 1600, "h")                                # stue nord vest-del
    vindu(8100, 0, 1600, "h")                               # kjøkken nord
    vindu(0, 1000, 1600, "v")                               # stue vest (mot terrasse)
    vindu(0, 5300, 1300, "v")                               # sov vest
    vindu(1300, 8500 - YV, 1300, "h")                       # sov sør
    vindu(10999 - YV, 200, 0, "v") if False else None
    vindu(11000 - YV, 300, 700, "v")                        # stue øst lite
    # dører
    door(5000, 0, 1000, YV, "h", "start", "inn")                          # hovedinngang nord
    door(4700, 8500 - YV, 900, YV, "h", "start", "ut")                    # inngang sør (VF)
    door(0, 2900, 900, YV, "v", "start", "inn", gulv=PARKETT)             # terrassedør vest
    door(4000, 5300, 890, IV, "v", "start", "ut", gulv=PARKETT)           # sov
    door(9000, 5300, 800, IV, "v", "start", "inn", gulv=FLIS)             # wc
    door(11000 - YV, 7650, 800, YV, "v", "start", "ut", gulv=BETONG)      # hus -> garasje
    # garasjeport (øst)
    r(17000 - YV, 2900, YV, 2600, "#FDFBF7")
    linje(17000 - YV + 40, 2900, 17000 - YV + 40, 5500, MORK, 34)
    linje(17000 - 40, 2900, 17000 - 40, 5500, MORK, 34, dash="200 120")
    # trapp
    trapp(4800, 4900, 1800, 2500, opp="n", trinn=10, tekst_under=False)
    tekst(7900, 5100, "OPP/NED", 170, GRAA, 500)
    # møblering — stue/kjøkken
    hylle(6800, 300, 4000, 620)                             # kjøkkenrekke nord
    komfyr(8600, 320, 520)
    vask(10250, 620, 170)
    hylle(10400, 900, 550, 1900)                            # kjøkken øst-del
    bord(3300, 1300, 2600, 1150, rx=300)                    # spisebord
    for sx in (3550, 4350, 5150):
        stol(sx, 830); stol(sx, 2500)
    stol(2830, 1650); stol(5950, 1650)
    sofa(500, 500, 2300, 950, rygg="n")
    bord(1100, 1750, 1000, 600, rx=150)
    teppe(400, 1600, 2400, 1100)
    hylle(700, 3900, 1800, 420)                             # tv-benk mot sov-vegg
    # møblering — sov
    seng(500, 5200, 1800, 2100)
    nattbord(150, 5230); nattbord(2350, 5230)
    garderobe(2900, 5000, 550, 2200)
    # møblering — vf
    teppe(4600, 7850, 1100, 500)
    hylle(6400, 7950, 800, 420)
    # møblering — wc
    toalett(9250, 4850, "n")
    vask(10350, 5050, 160)
    vaskemaskin(10250, 6550, 600)
    # garasje: markering
    tekst(14000, 4200, "Garasje", 340, MORK, 600)
    tekst(14000, 4560, "36,6 m²", 250, GRAA, 400)
    tekst(14000, 5000, "Betonggulv", 210, GRAA, 400)
    # terrasse & innganger
    tekst(-1350, 4200, "Terrasse", 280, GRAA, 600)
    tekst(-1350, 4520, "22,5 m²", 220, GRAA, 400)
    bord(-2100, 1200, 850, 850, rx=425)
    stol(-2300, 2200); stol(-1000, 1000)
    tekst(5500, -550, "Inngang", 220, GRAA, 500)
    tekst(5000, 9250, "Bislag", 220, GRAA, 500)
    # romnavn
    romnavn(3800, 3600, "Stue/Kjøkken")
    romnavn(2000, 6900, "Sov")
    romnavn(7800, 7900, "VF", 12.2, s1=280, s2=210)
    tekst(10000, 6200, "WC", 240, MORK, 600); tekst(10000, 6470, "4,3 m²", 190, GRAA, 400)
    sone(1600, -350, "1. ETASJE · BRA 84 M²")

    skriv("1. etasje", "-3400 -2000 21200 13000", (-3200, 10500))


# ================================================================ 2. ETASJE
# Hovedblokk 11000x8500, takterrasse øst 11000-17000 (42,7 m²).
def etg2():
    deler.append('<path d="M 0 0 H 11000 V 8500 H 0 Z" fill="#FDFBF7" filter="url(#skygge)"/>')
    # takterrasse
    r(11000, 300, 6000, 7900, "url(#dekke)")
    deler.append(f'<rect x="11000" y="300" width="6000" height="7900" fill="none" '
                 f'stroke="{GRAA}" stroke-width="26" stroke-dasharray="240 140"/>')
    # gulv
    r(0, 0, 11000, 8500, "url(#parkett)")
    r(3900, 5300, 2400, 3200, "url(#flis)")                 # bad 5.7
    r(8000, 5300, 3000, 3200, "url(#flis)")                 # bad 7.8
    # yttervegger
    r(0, 0, 11000, YV, MORK)
    r(0, 0, YV, 8500, MORK)
    r(0, 8500 - YV, 11000, YV, MORK)
    r(11000 - YV, 0, YV, 8500, MORK)
    # innervegger
    r(3700, 0, IV, 3400, MORK)                              # sov11.2 | sov9.9
    r(6600, 0, IV, 3400, MORK)                              # sov9.9 | sov6.9
    r(9100, 0, IV, 3400, MORK)                              # sov6.9 | gang-øst
    r(0, 3400, 11000, IV, MORK)                             # topprad sør (mot gang)
    r(2600, 3400, IV, 1900, MORK)                           # gard øst
    r(0, 5300, 11000, IV, MORK)                             # gang sør
    r(3900, 5300, IV, 3200, MORK)                           # sov12.8 | bad5.7
    r(6300, 5300, IV, 3200, MORK)                           # bad5.7 | trapp/gang-sone
    r(8000, 5300, IV, 3200, MORK)                           # | bad7.8
    # vinduer
    vindu(1000, 0, 1400, "h")                               # sov 11.2
    vindu(4500, 0, 1400, "h")                               # sov 9.9
    vindu(7300, 0, 1200, "h")                               # sov 6.9
    vindu(0, 1100, 1300, "v")                               # sov 11.2 vest
    vindu(0, 6300, 1300, "v")                               # sov 12.8 vest
    vindu(1300, 8500 - YV, 1300, "h")                       # sov 12.8 sør
    vindu(4600, 8500 - YV, 1000, "h")                       # bad 5.7 sør
    vindu(8800, 8500 - YV, 1200, "h")                       # bad 7.8 sør
    # dører
    door(700, 3400, 890, IV, "h", "end", "ut", gulv=PARKETT)              # sov 11.2
    door(4100, 3400, 890, IV, "h", "start", "ut", gulv=PARKETT)           # sov 9.9
    door(7000, 3400, 890, IV, "h", "start", "ut", gulv=PARKETT)           # sov 6.9
    door(9500, 3400, 890, IV, "h", "start", "ut", gulv=PARKETT)           # gard-øst
    door(2600, 3900, 800, IV, "v", "start", "inn", gulv=PARKETT)          # gard
    door(2950, 5300, 890, IV, "h", "start", "inn", gulv=PARKETT)          # sov 12.8
    door(4400, 5300, 800, IV, "h", "start", "inn", gulv=FLIS)             # bad 5.7
    door(8400, 5300, 800, IV, "h", "start", "inn", gulv=FLIS)             # bad 7.8
    door(11000 - YV, 3900, 900, YV, "v", "start", "ut", gulv=DEKKE)       # dør -> takterrasse
    # trapp
    trapp(6500, 5500, 1400, 2400, opp="s", trinn=10, tekst_under=False)
    tekst(7200, 5150, "NED", 170, GRAA, 500)
    # møblering — soverom topprad
    seng(400, 500, 1600, 2000); garderobe(2700, 300, 550, 1700)
    seng(4300, 500, 1500, 2000); garderobe(5900, 300, 550, 1500)
    seng(7000, 500, 1300, 1900); garderobe(8400, 300, 550, 1300)
    # gard + gang
    garderobe(300, 3700, 550, 1400); garderobe(1800, 3700, 550, 1400)
    teppe(3300, 4100, 4200, 700)
    # gard-øst (walk-in)
    garderobe(10250, 300, 550, 1600)
    garderobe(9350, 250, 1500, 0) if False else None
    tekst(9800, 2600, "Gard.", 220, GRAA, 500)
    # sov 12.8
    seng(900, 5450, 1800, 2100)
    nattbord(400, 5480)
    garderobe(3300, 6900, 550, 1450)
    # bad 5.7
    dusj(4100, 7400, 850)
    vask(4900, 5900, 160)
    toalett(5600, 5500, "n")
    # bad 7.8
    badekar(9100, 5600, 750, 1700) if False else badekar(8300, 5550, 1700, 750)
    dusj(10000, 7400, 850)
    vask(8700, 7800, 160)
    toalett(8200, 6600, "n") if False else toalett(8300, 6550, "n")
    # takterrasse
    sofa(12000, 1200, 2600, 950, rygg="n")
    bord(12800, 2600, 1000, 650, rx=150)
    bord(14500, 5200, 1000, 1000, rx=500)
    stol(14000, 4700); stol(15600, 5450)
    # romnavn
    romnavn(1800, 2700, "Sov", 11.2)
    romnavn(5300, 2700, "Sov", 9.9)
    romnavn(8000, 2700, "Sov", 6.9)
    tekst(1300, 4550, "Gard. 5 m²", 210, GRAA, 500)
    romnavn(4900, 4550, "Gang", 14.9, s1=270, s2=0) if False else tekst(4900, 4400, "Gang 14,9 m²", 250, MORK, 600)
    romnavn(1800, 7950, "Sov", 12.8)
    tekst(5300, 6600, "Bad", 260, MORK, 600); tekst(5300, 6890, "5,7 m²", 200, GRAA, 400)
    tekst(9800, 6900, "Bad", 260, MORK, 600); tekst(9800, 7190, "7,8 m²", 200, GRAA, 400)
    romnavn(14000, 3900, "Takterrasse", 42.7)
    sone(1600, -350, "2. ETASJE · BRA 84 M²")

    skriv("2. etasje", "-700 -1100 18500 11400", (-500, 9800))


uetg()
etg1()
etg2()
