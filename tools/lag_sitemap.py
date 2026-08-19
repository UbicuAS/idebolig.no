"""
Lager sitemap.xml og robots.txt for idebolig.no.

WordPress serverte tidligere begge deler dynamisk (wp-sitemap.xml og en
virtuell robots.txt). Etter overgangen til statisk side må de lages her.

Sidene under er de kanoniske. Utelatt med vilje:
  /boligkatalog-ny/  — canonical peker allerede til /vaare-boliger/
  /edvard.html       — duplikat av /edvard/

Kjøres fra rotmappen:  python tools/lag_sitemap.py
"""
import subprocess
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote

ROT = Path(__file__).resolve().parent.parent
BASIS = "https://idebolig.no"

# (sti i repoet, URL-sti, prioritet, endringsfrekvens)
SIDER = [
    ("index.html",                 "/",                1.0, "monthly"),
    ("våre-boliger/index.html",    "/våre-boliger/",   0.9, "monthly"),
    ("tjenester/index.html",       "/tjenester/",      0.8, "monthly"),
    ("prosjekter/index.html",      "/prosjekter/",     0.8, "monthly"),
    ("boligkatalog/index.html",    "/boligkatalog/",   0.7, "yearly"),
    ("alva/index.html",            "/alva/",           0.7, "yearly"),
    ("edvard/index.html",          "/edvard/",         0.7, "yearly"),
    ("edvard-prakt/index.html",    "/edvard-prakt/",   0.7, "yearly"),
    ("embla/index.html",           "/embla/",          0.7, "yearly"),
    ("nora/index.html",            "/nora/",           0.7, "yearly"),
    ("odin/index.html",            "/odin/",           0.7, "yearly"),
    ("tiril/index.html",           "/tiril/",          0.7, "yearly"),
    ("vilde/index.html",           "/vilde/",          0.7, "yearly"),
    ("til-salgs/index.html",       "/til-salgs/",      0.6, "monthly"),
    ("about/index.html",           "/about/",          0.6, "yearly"),
    ("kontakt/index.html",         "/kontakt/",        0.6, "yearly"),
]


def sist_endret(rel: str) -> str:
    """Dato for siste commit som rørte fila. Faller tilbake på filens
    tidsstempel hvis git ikke vet — SMB-delingen gjør mtime upålitelig,
    så git er den beste kilden vi har."""
    try:
        ut = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel],
            cwd=ROT, capture_output=True, text=True, timeout=20,
        )
        stamp = ut.stdout.strip()
        if stamp:
            return stamp
    except Exception:
        pass
    try:
        return datetime.fromtimestamp((ROT / rel).stat().st_mtime).strftime("%Y-%m-%d")
    except OSError:
        return date.today().isoformat()


linjer = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]

manglende = []
for rel, url, pri, frekvens in SIDER:
    if not (ROT / rel).exists():
        manglende.append(rel)
        continue
    # Æ, Ø og Å må prosentkodes i sitemap-URLer
    trygg = quote(url, safe="/")
    linjer += [
        "  <url>",
        f"    <loc>{BASIS}{trygg}</loc>",
        f"    <lastmod>{sist_endret(rel)}</lastmod>",
        f"    <changefreq>{frekvens}</changefreq>",
        f"    <priority>{pri:.1f}</priority>",
        "  </url>",
    ]
    print(f"  {url}")

linjer.append("</urlset>")
(ROT / "sitemap.xml").write_text("\n".join(linjer) + "\n", encoding="utf-8")

(ROT / "robots.txt").write_text(
    "User-agent: *\n"
    "Allow: /\n"
    "\n"
    f"Sitemap: {BASIS}/sitemap.xml\n",
    encoding="utf-8",
)

print(f"\nsitemap.xml skrevet med {len(SIDER) - len(manglende)} sider")
print("robots.txt skrevet")
if manglende:
    print("\nFANT IKKE (utelatt fra sitemap):")
    for m in manglende:
        print("  " + m)
