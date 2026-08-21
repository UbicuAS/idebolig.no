#!/usr/bin/env python3
"""Lager permbildet til «Boligkatalog 2026»: katalog-2026-h7vq3kfm/permforside.webp

Permen er stående 510×680 (3:4), mens alle fasadebildene er 16:9. Å legge inn
originalen og la object-fit:cover beskjære ville lastet 3,1 MB PNG for å vise
42 % av bredden. I stedet beskjæres bildet ferdig til 3:4 og lagres som WebP i
2× oppløsning (1020×1360) — nok til skjermer med DPR 2 på standardstørrelse.

Valget av motiv: Edvard Prakt står best i stående format. Vilde og Nora
beskjæres til terrasse og hagemøbler, Embla og Odin havner skjevt i ramma.

Kjør på nytt hvis motivet skal byttes — endre KILDE og bygg katalogen etterpå.
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
KILDE = ROOT / "wp-content/uploads/2025/03/Fasade-fremside.png"   # Edvard Prakt
MÅL = ROOT / "katalog-2026-h7vq3kfm/permforside.webp"

BREDDE, HØYDE = 1020, 1360          # 2× av permens 510×680
KVALITET = 82


def main() -> None:
    with Image.open(KILDE) as im:
        im = im.convert("RGB")
        forhold = BREDDE / HØYDE
        ny_bredde = round(im.height * forhold)
        if ny_bredde > im.width:                     # smalere kilde enn 3:4
            ny_høyde = round(im.width / forhold)
            topp = (im.height - ny_høyde) // 2
            utsnitt = im.crop((0, topp, im.width, topp + ny_høyde))
        else:
            venstre = (im.width - ny_bredde) // 2    # sentrert, som object-fit
            utsnitt = im.crop((venstre, 0, venstre + ny_bredde, im.height))
        utsnitt = utsnitt.resize((BREDDE, HØYDE), Image.LANCZOS)
        utsnitt.save(MÅL, "WEBP", quality=KVALITET, method=6)

    kb = MÅL.stat().st_size / 1024
    kilde_kb = KILDE.stat().st_size / 1024
    print(f"Skrev {MÅL.relative_to(ROOT)} — {BREDDE}×{HØYDE}, {kb:.0f} KB "
          f"(kilde {kilde_kb:.0f} KB)")


main()
