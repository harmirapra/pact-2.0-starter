---
name: personal-voice-analyst
description: >-
  Z tvých vlastních textů — e-mailů, zpráv, poznámek, příspěvků — vytáhne, jak píšeš,
  a naplní tím 2_Context/identity/tone-of-voice/. Vedle stylu vytěží i opakující se
  myšlenkové postupy a názory, které stojí za sdílení.
  Use when: uživatel řekne "zjisti, jak píšu", "analyzuj můj styl", "naplň tone of voice",
  "vytvoř mi tone of voice", "z čeho poznáš můj styl", "analyze my writing style",
  "build my tone of voice". Nabídni ji sám, když je tone-of-voice/ prázdný a uživatel
  chce, aby něco znělo jako on.
---

# Personal voice analyst

Šablona PACT přijde na nový stroj prázdná. Tohle je dovednost, která ji naplní tou jedinou věcí, kterou PACT instaluje do `$HOME` — tvým hlasem.

Rozdíl proti běžnému „napiš mi tone of voice": tenhle postup **nevymýšlí**. Každý závěr stojí na citaci z tvého skutečného textu.

## Co potřebuješ na vstupu

Cokoli, co uživatel opravdu napsal:

- export chatu nebo pracovní komunikace
- odeslané e-maily
- poznámky, zápisy, dokumenty
- příspěvky na sociálních sítích, články

**Kolik:** čím víc, tím lépe, ale i dvacet delších zpráv dá použitelný výsledek. Pod deset textů výsledek nedělej — řekni, že to je málo, a vysvětli proč: styl se pozná z opakování, ne z jednoho textu.

**Co s materiálem udělej dřív, než začneš:** odstraň systémové zprávy a metadata, zahoď duplicity, ale **zachovej kontext** — datum, komu to bylo psané, jestli to bylo veřejné nebo soukromé. Styl se mění podle publika a to je samo o sobě nález.

## Zpracování dat

Když je materiálu hodně a máš možnost spustit kód, napiš si na přípravu krátký skript — vytáhne texty, spočítá délky vět, najde nejčastější obraty. Je to spolehlivější než odhad od oka.

**Když kód spustit nemůžeš**, čti materiál přímo a citace si veď průběžně. Nedělej statistiku odhadem — když nemáš čím spočítat „průměrná délka věty", nepiš žádné číslo.

## Co hledat

### 1. Jak zní

| Rozměr | Co v textu sledovat |
|---|---|
| Základní tón | formální/neformální, klidný/energický, přátelský/věcný |
| Jazykové vzorce | slova, která se vracejí; charakteristické obraty; délka vět |
| Emoce | jak vyjadřuje nadšení, nesouhlas, pochvalu, frustraci |
| Přizpůsobení | jak se styl mění podle příjemce |
| Poznávací znamení | co dělá ten hlas rozpoznatelným |

### 2. Jak přemýšlí

Opakující se myšlenkové postupy — jaké rámce používá, jaká přirovnání, jak se rozhoduje, co v problému hledá první. Tohle je často cennější než styl, protože se to nedá odkoukat.

### 3. Co má cenu sdílet

Průběžně si všímej míst, kde uživatel řekl něco, co má hodnotu i mimo původní kontext: vlastní postřeh, praktická rada, poučení z chyby, názor, který jde proti proudu.

## Tvrdá pravidla

- **Každý závěr má nejméně dvě citace.** Bez důkazu se závěr nepíše.
- **Žádné obecné hodnocení.** „Efektivní komunikátor", „přirozený leader" — to jsou fráze, které sedí na kohokoli. Když nemůžeš tvrzení podložit konkrétním místem, není to nález.
- **Nevyhlazuj.** Když někdo píše dlouhá souvětí a používá závorky, patří to do popisu stylu, i kdyby to bylo „proti pravidlům".
- **Zachovej jazyk.** Analyzuješ-li české texty, výstup je česky a citace zůstávají doslovné.

## Výstup

Dovednost produkuje **dva různé výstupy** a je potřeba je nesplést.

### A) Soubory pro `2_Context/identity/tone-of-voice/`

Tohle je hlavní výstup — přímo použitelná pravidla, ne popis.

```markdown
# Tone of voice

## Jak píšu
[3–6 vět. Jak text zní, když ho píšu já.]

## Používám
- [obrat] — např. "[citace]"
- [obrat] — např. "[citace]"

## Nepoužívám
- [čemu se vyhýbám] — protože [z čeho je to vidět]

## Délka a stavba
[Věty, odstavce, jestli používám odrážky, nadpisy, zvýraznění.]

## Podle příjemce
| Komu | Jak se to mění |
```

Když je materiálu dost na rozlišení kanálů, rozděl to na víc souborů — třeba `email.md`, `interni.md`, `verejne.md` — a nech `general.md` jako společný základ.

### B) Report do `0_Projects/<projekt>/` nebo `2_Context/expertise/`

Delší analýza — myšlenkové postupy, silné stránky s důkazy, sbírka věcí, které mají cenu sdílet. Tohle **nepatří** do `tone-of-voice/`, protože se to načítá při každém psaní a je to zbytečná zátěž.

## Než výstup odevzdáš

| Test | Otázka |
|---|---|
| Důkaz | Má každý závěr aspoň dvě citace? |
| Konkrétnost | Sedí některé tvrzení stejně dobře na kohokoli jiného? Pak ho smaž. |
| Použitelnost | Dokáže podle `tone-of-voice/` jiný agent napsat text, který zní jako uživatel? |
| Věrnost | Nevyhladil jsem autora do neutrální podoby? |

Poslední test je ten nejdůležitější. Výsledek, který zní jako obecná rada, jak psát dobře, je selhání.

## Když nedosáhneš na materiál

Uživatel často řekne „analyzuj můj styl" a žádné texty nepřiloží. Neodhaduj a nevymýšlej. Zeptej se a nabídni konkrétní zdroje: odeslaná pošta za poslední měsíc, poznámky v PACT, cokoli delšího, co psal. Když nic není, řekni, že bez materiálu tahle dovednost nedává výstup.
