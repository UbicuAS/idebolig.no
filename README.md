# Idébolig — nettside

Statisk nettside for [idebolig.no](https://idebolig.no). Bygget fra en speiling av
den gamle WordPress-siden (Astra + Elementor, speilet 5. august 2026), deretter
redesignet side for side.

**I drift:** https://idebolig.no — statiske filer på Domeneshops webhotell,
lansert 12. august 2026.
**Forhåndsvisning:** https://idebolig.ubicu.cloud/ (GitHub Pages, deploy fra `main`)

WordPress ligger arkivert på webhotellet i `~/wordpress-arkiv-2026-08-12/` med
databasen urørt. Rullback er å flytte to mapper tilbake.

## ⚠️ E-posten røres ikke

Ingenting i e-postoppsettet til idebolig.no skal endres — ikke MX, ikke SPF, ikke
autodiscover, ikke DMARC. Heller ikke «ufarlige» opprydninger. Domenet tilhører
kunden. Hele grunnen til at siden ligger på webhotellet framfor GitHub Pages er at
det ikke krever en eneste DNS-endring.

## Status

- 17 sider: forside, om oss, tjenester, prosjekter, kontakt, boligkatalog,
  våre boliger og husmodellene Alva, Edvard, Edvard Prakt, Embla, Nora, Odin,
  Tiril og Vilde.
- Ekte foto lagt inn (52 av 63 plasser; resten droppet etter avtale).
- Kontaktskjemaet går til `skjema.php` med Cloudflare Turnstile og seks lag
  spamvern. Hemmelighetene ligger i `~/skjema-config.php`, utenfor webroten.
  Bekreftet virksomt av kunden 12. aug.
- Ingen Google-sporing og ingen tredjeparts skript. Analytics, Site Kit,
  WPForms og reCAPTCHA er fjernet.
- `sitemap.xml` og `robots.txt` vedlikeholdes av `tools/lag_sitemap.py`.

## Arbeidsflyt

Endringer gjøres på egen branch, ikke rett på `main`:

    branch → passordbeskyttet forhåndsvisning på idebolig.no/forhandsvis/
           → godkjenning → merge til main → utlegging

Utlegging skjer med SSH/rsync til webhotellet (bruker `idebolig` på
`login.domeneshop.no`). Ikke legg ut uten at Marius har bedt om det.

## Lokal kjøring

```
python -m http.server 8741
```

Registrert som `idebolig` i `.claude/launch.json`. Merk at kontaktskjemaet krever
PHP og bare kjører på idebolig.no — lokalt og på forhåndsvisningen viser det en
vennlig beskjed i stedet for å sende.

## Struktur

- `index.html` + undermapper per side
- `wp-content/`, `wp-includes/` — tema- og plugin-assets fra speilingen
- `prosjekt-assets/` — bilder og video til prosjektsiden
- `skjema.php` — kontaktskjemaets endepunkt (ligger i webroten på serveren)
- `tools/` — generatorskriptene. **Ligger utenfor webroten på serveren.**
  Endres en side som et skript har generert, endres skriptet — ikke HTML-en.

## Backlog og rapporter

Backlog (IB1.1, IB2.1, IB3.1 …) og rapporter vedlikeholdes på claude-delingen:
`Prosjekter/Idebolig/` (RAPPORT-MARIUS.md og RAPPORT-SANGAR.md).
Arbeidslogg: `nettside-Roar/LOGG.md`.
