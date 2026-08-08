---
name: rpi-research
description: >-
  První fáze RPI (Research → Plan → Implement → Review) — přemění nejistotu
  o existujícím kódu nebo API v ověřenou znalost, zapsanou do souboru.
  Nikdy nepíše ani neupravuje kód.
  Use when: uživatel řekne "rozjeď RPI", "začni research fází", "nejdřív
  prozkoumej, jak to tam funguje", "start RPI research", "research this
  before we plan", nebo se chystáš implementovat něco, čemu ještě
  nerozumíš (nový vzor, cizí API, nejasné zadání) — v tom případě RPI
  aktivně nabídni, viz AGENTS.md.
---

# RPI — Research

Cíl týhle fáze: **ověřená znalost na disku**, ne dojem v hlavě. Konec fáze pozná podle toho, že by výsledek dal smysl i někomu, kdo se k tématu vrátí za měsíc bez tebe.

## Tvrdé pravidlo

**V týhle fázi NIKDY nepiš ani neupravuj kód.** Ani „jen na vyzkoušení", ani „jen abych ověřil hypotézu". Jakmile začneš psát kód, přestáváš zkoumat a začínáš implementovat — a to je jiná fáze, s jinými zárukami. Když zjistíš, že bez spuštění kódu nejde ověřit hypotéza, napiš to do zjištění a nech na fázi Plan nebo Implement, aby to udělala.

Vynucuje se instrukcí, ne omezením nástrojů — dovednost nemá jak agentovi sebrat přístup k editoru. Když sám sebe přistihneš, že píšeš kód, zastav se a vrať se k otázce, kterou máš zodpovědět.

## Postup

1. **Zformuluj otázky.** Co přesně potřebuješ vědět, než půjde plánovat? Konkrétní otázky, ne „prozkoumej X obecně".
2. **Hledej v kódu, ne v paměti.** Otevři skutečné soubory, přečti skutečné API, spusť jen read-only příkazy (`grep`, čtení, dokumentace). Domněnka bez ověření v kódu se do zjištění nepočítá.
3. **Zaznamenávej i to, co jsi vyvrátil.** „Předpokládal jsem X, ale je to jinak — Y" je stejně cenné jako potvrzená hypotéza. Bez toho příští čtenář zopakuje tvou první, špatnou domněnku.
4. **Přiznej mezery.** Co se nepodařilo zjistit a proč (nedostupný zdroj, nejasná odpověď, protichůdné zdroje) patří do výstupu stejně jako zjištěná fakta.

## Výstup

`0_Projects/<projekt>/rpi/RRRR-MM-DD-<téma>-research.md`:

```markdown
# Research: <téma>

## Otázky
- ...

## Zjištění
- <tvrzení> — <kde je to ověřené: soubor:řádek, dokumentace, test>

## Vyvrácené domněnky
- <co se čekalo> → <co je ve skutečnosti>

## Otevřené mezery
- <co zůstává nejisté a proč>
```

## Než skončíš

Zkontroluj, že u každého zjištění je odkaz na konkrétní soubor a řádek, ne jen slovní popis. Plán, který na tohle naváže, potřebuje umět zjištění ověřit sám, ne ti věřit na slovo.

## Kritické pravidlo: vyčisti kontext před další fází

Fáze Plan **nesmí** dědit tuhle konverzaci. Otevři novou konverzaci (nebo `/clear`) a předej jí jen výstupní soubor, ne historii chatu. Nahromaděný kontext způsobí, že Plan podědí tvoje domněnky místo toho, aby si ověřil zjištění sám ze souboru — a to je přesně to, čemu má RPI zabránit.
