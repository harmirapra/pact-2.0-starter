---
name: rpi-review
description: >-
  Čtvrtá a poslední fáze RPI (Research → Plan → Implement → Review) —
  nezávisle prověří, že implementace odpovídá plánu a skutečně funguje.
  Use when: uživatel řekne "zkontroluj tu implementaci", "rpi review",
  "review the changes", "did this actually work", nebo odevzdá hotový
  `*-changes.md` a chce uzavřít cyklus RPI.
  Nepoužívej na obecnou kontrolu textu/výstupu bez vazby na implementační
  plán — na to je quality-gate.
---

# RPI — Review

Cíl týhle fáze: nezávislé ověření, ne zdvořilostní potvrzení. Review, které jen shrne, co implementace tvrdí, že udělala, review není.

## Vstup

Přečti `*-plan.md` a `*-changes.md` **jako soubory**, v nové konverzaci (viz kritické pravidlo v `rpi-implement`). Pak si nezávisle projdi skutečný kód — nevěř shrnutí v `changes.md`, ověř ho.

## Postup

1. **Porovnej plán se skutečností.** Odpovídá to, co je v kódu, tomu, co plán chtěl? Odchylky zapsané v `changes.md` — dávají smysl, nebo jsou to tiché náhrady bez zdůvodnění?
2. **Spusť, co se dá spustit.** Testy, lint, ruční ověření kroku, který popisoval hraniční případ. Tvrzení „funguje to" bez spuštění se do review nepočítá.
3. **Hledej, co plán nezachytil.** Nový kód mohl zavést vedlejší efekt, který ani research, ani plán nepředvídaly — review je poslední místo, kde se to dá chytit před tím, než jde dál.
4. **Verdikt je binární: prošlo, nebo neprošlo s konkrétním důvodem.** „Vypadá to dobře" není verdikt.

## Výstup

`0_Projects/<projekt>/rpi/RRRR-MM-DD-<téma>-review.md`:

```markdown
# Review: <téma>

Vychází z: RRRR-MM-DD-<téma>-plan.md, RRRR-MM-DD-<téma>-changes.md

## Ověřeno
- <co bylo spuštěno/zkontrolováno> — <výsledek>

## Nálezy
- <nález> — <závažnost> — <doporučená akce>

## Verdikt
PROŠLO / NEPROŠLO — <jednořádkové zdůvodnění>
```

## Když review neprojde

Nálezy jdou zpátky — buď jako nový krok pro `rpi-implement` (drobná oprava), nebo jako podnět pro nový cyklus `rpi-research`/`rpi-plan` (ukázalo se, že plán stál na chybném předpokladu). Review samo kód neopravuje — to by ho vrátilo do role implementace bez nezávislého ověření.

## Uzavření cyklu

Po úspěšném review shrň v `0_Projects/<projekt>/architecture.md` získanou znalost (povinná retrospektiva z `AGENTS.md`) — RPI proběhlo pro *tenhle* úkol, ale poznatek z něj má přežít i po něm.
