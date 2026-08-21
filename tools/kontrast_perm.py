#!/usr/bin/env python3
"""Måler tekstkontrasten på katalogpermen i stedet for å vurdere den på øyemål.

Permen har et fotografi bak en gradering. Om teksten er lesbar avhenger av hvor
lyst motivet er nettopp der teksten ligger — det er ikke noe man ser sikkert ved
å skule på et skjermbilde. Skriptet legger den samme graderingen som CSS-en over
bildet, og regner WCAG-kontrast for hver tekstlinje mot bakgrunnen bak den.

Grensene: 4,5:1 er kravet for vanlig tekst (WCAG AA), 3:1 for stor tekst.
Vi sikter mot 7:1 (AAA) på den lille hinttekster nederst, som er minst.
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BILDE = ROOT / "katalog-2026-h7vq3kfm/permforside.webp"

# Samme stopp som i .fb-perm--foto::after — hold disse i synk med generatoren.
STOPP = [(0.00, 0.90), (0.30, 0.72), (0.60, 0.75), (1.00, 0.95)]
OVER = (22, 20, 17)

# Omtrentlig plassering av hvert tekstelement, som andel av permhøyden,
# målt i nettleseren på standardstørrelse (510×680).
TEKST = [
    ("logo (hvit)",        0.255, 0.345, "#FFFFFF", 3.0),
    ("«Boligkatalog»",     0.435, 0.495, "#FFFFFF", 3.0),
    ("«2026»",             0.505, 0.545, "#C99C55", 3.0),
    ("undertittel",        0.560, 0.600, "#D9D2C5", 4.5),
    ("blahint (minst)",    0.640, 0.670, "#D9D2C5", 4.5),
]


def alfa(y: float) -> float:
    for (y1, a1), (y2, a2) in zip(STOPP, STOPP[1:]):
        if y1 <= y <= y2:
            t = 0 if y2 == y1 else (y - y1) / (y2 - y1)
            return a1 + (a2 - a1) * t
    return STOPP[-1][1]


def lum(rgb) -> float:
    def kanal(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (kanal(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def kontrast(a, b) -> float:
    l1, l2 = sorted((lum(a), lum(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def hex_rgb(s):
    return tuple(int(s[i:i + 2], 16) for i in (1, 3, 5))


def main() -> None:
    with Image.open(BILDE) as im:
        im = im.convert("RGB")
        b, h = im.size
        alt_ok = True
        print(f"{BILDE.name} — {b}×{h}\n")
        print(f"{'element':20s} {'alfa':>6s} {'bakgrunn':>16s} {'kontrast':>9s}  krav")
        for navn, y1, y2, farge, krav in TEKST:
            # verste (lyseste) piksel i båndet avgjør lesbarheten
            bånd = im.crop((0, int(y1 * h), b, int(y2 * h)))
            små = bånd.resize((24, 6), Image.LANCZOS)
            verst, verst_a = None, None
            for j in range(6):
                y = (y1 + (y2 - y1) * (j + 0.5) / 6)
                a = alfa(y)
                for i in range(24):
                    px = små.getpixel((i, j))
                    blandet = tuple(round(p * (1 - a) + o * a) for p, o in zip(px, OVER))
                    if verst is None or lum(blandet) > lum(verst):
                        verst, verst_a = blandet, a
            k = kontrast(hex_rgb(farge), verst)
            ok = k >= krav
            alt_ok &= ok
            merke = "OK" if ok else "FOR LAVT"
            print(f"{navn:20s} {verst_a:6.2f} {str(verst):>16s} {k:8.2f}:1  ≥{krav} {merke}")
        print("\n" + ("Alle tekstelementer er over kravet." if alt_ok
                      else "MINST ETT ELEMENT ER UNDER KRAVET — juster graderingen."))


main()
