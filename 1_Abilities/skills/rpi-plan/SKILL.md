---
name: rpi-plan
description: >-
  Druhá fáze RPI (Research → Plan → Implement → Review) — přemění ověřenou
  znalost z research fáze na krokovatelnou strategii s odkazy na konkrétní
  soubory a řádky. Nikdy nepíše ani neupravuje kód.
  Use when: uživatel řekne "naplánuj to", "udělej z toho research plánu",
  "rpi plan", "write the implementation plan", "plan this out", nebo
  odevzdá hotový `*-research.md` a chce pokračovat další fází RPI.
---

# RPI — Plan

Cíl týhle fáze: **strategie, kterou by mohl provést i někdo jiný**, protože každý krok míří na konkrétní místo v kódu, ne na obecný záměr.

## Tvrdé pravidlo

**V týhle fázi NIKDY nepiš ani neupravuj kód.** Plán popisuje, co se má stát — neprovádí to. Když si nejsi jistý, jestli je krok proveditelný, ověř to čtením kódu (dovoleno), ne zkušebním zápisem (zakázáno).

## Vstup

Přečti `*-research.md` z předchozí fáze **jako soubor**, ne z paměti konverzace — pokud jsi ve stejné konverzaci, ve které vznikl research, něco jsi udělal špatně (viz kritické pravidlo v `rpi-research`). Pokud research chybí nebo je neúplný, řekni to a navrhni doplnit ho, než budeš plánovat na dohady.

## Postup

1. **Rozděl cíl na kroky.** Každý krok: co se změní, ve kterém souboru, jaký je výsledek po tomhle kroku (ne až po celém plánu).
2. **U každého kroku odkaz na místo v kódu** — soubor a řádek nebo funkce, ne „uprav validaci". Krok bez konkrétního místa je znamení, že research nebyl dost hluboký; vrať se k němu, nedomýšlej.
3. **Pojmenuj rizika.** Co se může pokazit, na co plán spoléhá, co nebylo v research ověřené.
4. **Označ pořadí závislostí.** Které kroky musí proběhnout před kterými a proč.

## Výstup

`0_Projects/<projekt>/rpi/RRRR-MM-DD-<téma>-plan.md`:

```markdown
# Plan: <téma>

Vychází z: RRRR-MM-DD-<téma>-research.md

## Kroky
- [ ] 1. <co> — `soubor.py:42` — <očekávaný výsledek>
- [ ] 2. ...

## Závislosti
- krok 2 vyžaduje dokončený krok 1, protože ...

## Rizika
- <riziko> — <jak ho plán zmírňuje, nebo že se zmírnit nedá>
```

## Kritické pravidlo: vyčisti kontext před další fází

Fáze Implement dostane jen `*-plan.md` jako soubor, ne tuhle konverzaci. Nová konverzace nebo `/clear`. Implement, který podědí diskuzi o plánu místo aby četl hotový plán, může začít improvizovat kroky, které v plánu nejsou.
