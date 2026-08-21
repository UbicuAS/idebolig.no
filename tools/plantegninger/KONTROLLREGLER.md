# Kontrollregler for plantegninger

Skrevet 21.08.2026 etter Tiril-jobben, der samme tegning måtte rettes seks
ganger. Reglene finnes fordi hver runde skyldtes at jeg **gjettet** i stedet
for å **lese**. Les denne før du tegner, og kjør sjekklisten før levering.

---

## 0. Grunnregel: skaff riktig grunnlag først

**Be om målsatt PDF før du tegner en eneste strek.** Skjermbilder av CAD er
uleselige nok til å gi feil geometri, men lesbare nok til at man tror man har
forstått. Fire av seks Tiril-runder forsvant på dette.

- PDF finnes → les den som **vektor**, ikke som bilde:
  ```python
  import fitz                      # PyMuPDF
  d = fitz.open(pdf)
  d[0].get_text("words")           # romnavn + arealer MED koordinater
  d[0].get_drawings()              # alle linjesegmenter = veggenes faktiske geometri
  d[0].get_pixmap(matrix=fitz.Matrix(6,6), clip=fitz.Rect(...))   # zoom på detaljer
  ```
- Bare skjermbilde tilgjengelig → **si fra at presisjonen blir begrenset**, og
  be om PDF. Ikke lever «nesten riktig» i stillhet.
- Kalibrer alltid skalaen mot en kjent målkjede
  (`mm_pr_punkt = kjent_mål_i_mm / avstand_i_pdf_punkter`) før du måler noe.

## 1. Geometrien er ikke rettvinklet før du har bevist det

Moderne hus har hakk, utspring og skrå kanter. Antagelsen «det er en boks»
er den vanligste feilkilden.

- Gå langs **hele** ytterkonturen i tegningen og noter hvert hopp i veggliv.
  Tiril hadde et hakk på ~1000 mm midt på sørfasaden i begge etasjer.
- Sjekk **begge** langfasader og begge gavler. Feilen kan ligge på siden du
  ikke har sett på.
- Skrå linjer: hent dem ut som vektorer og les endepunktene. Ikke anslå
  vinkelen fra et bilde.
- Kryssjekk mot fasadebildene: et hakk i planen skal gi et synlig sprang i
  fasaden, og motsatt.

## 2. Arealene er fasit — regn før du tegner

Hvert rom har et oppgitt areal. Det er en **ligning** som geometrien må løse.

- Beregn arealet av formen du har tegnet (shoelace) og sammenlign:
  ```python
  def shoelace(p):
      a = 0
      for i in range(len(p)):
          x1, y1 = p[i]; x2, y2 = p[(i+1) % len(p)]
          a += x1*y2 - x2*y1
      return abs(a)/2/1e6        # m² når koordinatene er i mm
  ```
- Avvik > 2 % ⇒ formen er feil. Ikke «juster litt» — finn ut hva som er galt.
- **Ulike arealer i speilvendte enheter er et signal, ikke støy.** Tiril hadde
  balkonger på 9,8 og 7,8 m². Det kunne ikke oppstå ved speiling, og var
  beviset på at hakket lå på ulikt sted i de to enhetene.
- Like arealer ⇒ formen er speilsymmetrisk. Bruk det som kontroll.

## 3. Uterom: avklar tre ting eksplisitt

For hver terrasse/balkong, skriv ned svaret før du tegner:

1. **Inntrukket eller utstikkende?** Ligger den innenfor byggets fotavtrykk
   eller utenfor? (Tiril: bak = inntrukket, foran = utstikkende.)
2. **Har den vegger?** En overbygd uteplass har som regel *ingen* yttervegg —
   bare dekkekant og eventuelt rekkverk. Hatchet (massiv) vegg i tegningen =
   vegg; tynn strek = kant/takutstikk. **Tegn aldri vegg der tegningen viser
   tynn strek.**
3. **Hvor langt strekker den seg?** Går den over hele fasaden, eller bare i
   det inntrukne partiet? (Tiril: balkongen lå kun i hakket.)

## 4. Møblering skal være troverdig

Møbler er ikke dekorasjon — feil plassering ødelegger inntrykket av hele
tegningen. Sjekk hvert møbel mot dette:

- **Senger:** hodegjerdet skal ligge **inntil vegg**. Aldri midt på gulvet,
  aldri med hodet mot en dør eller et vindu. Ha fri passasje langs minst én
  langside. Nattbord bare der det faktisk er plass ved hodeenden.
- **Dørslag:** ingen møbler i sirkelsektoren en dør slår gjennom. Gå gjennom
  hver eneste dør.
- **Vegger:** ingen møbler som krysser en vegg eller stikker ut av rommet.
- **Vinduer:** ikke plasser høye møbler (skap) foran vinduer.
- **Speiling:** når en enhet speiles, må møblenes *retning* speiles sammen med
  posisjonen. Et hodegjerde «mot høyre» blir «mot venstre» i speilbildet.
- **Fri passasje:** det skal gå an å komme fra døra til vinduet uten å klatre.

## 5. Tekst og etiketter

- Romnavn og arealer skal ligge på **ledig gulv**, ikke oppå møbler,
  vegger eller andre etiketter.
- Etiketten skal ligge inne i rommet den beskriver.
- Kontroller i den ferdige renderingen — ikke i koden.

## Sjekkliste før levering

Gå gjennom punkt for punkt. Alle skal krysses av.

- [ ] Grunnlaget er målsatt PDF (eller mangelen er kommunisert til kunden)
- [ ] Skalaen er kalibrert mot en kjent målkjede
- [ ] Hele ytterkonturen er gjennomgått; alle hakk og sprang er med
- [ ] Begge langfasader og begge gavler er kontrollert
- [ ] Alle romarealer er shoelace-kontrollert mot tegningens tall (< 2 % avvik)
- [ ] Ulike arealer mellom speilvendte enheter er forklart, ikke ignorert
- [ ] For hvert uterom: inntrukket/utstikkende, vegg/ingen vegg, utstrekning
- [ ] Ingen møbler i dørslag
- [ ] Ingen møbler som krysser vegg eller stikker utenfor rommet
- [ ] Alle senger har hodegjerdet inntil vegg, klar av dør og vindu
- [ ] Møbelretning er speilet riktig i speilvendte enheter
- [ ] Ingen tekst ligger oppå møbler, vegger eller annen tekst
- [ ] Kryssjekket mot fasadebildene (hakk, balkonger, takform stemmer)
- [ ] Rendret i full størrelse og sett over visuelt, rom for rom

## Verktøynotat

- **Render:** Edge headless med egen `--user-data-dir` per kjøring, og
  `sleep` etter kallet. Uten det skrives filene asynkront og kan bli
  forrige kjørings innhold.
- **PyMuPDF kan ikke brukes til å rendre våre egne SVG-er** — den støtter
  ikke `<pattern>`, så gulvene blir svarte. Bruk Edge.
- Generatorene ligger i `tools/plantegninger/`. Alle bygger på
  `alva_helpers.py` (farger, møbelsymboler, vegger, dører, vinduer).
