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


