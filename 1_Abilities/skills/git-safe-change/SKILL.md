---
name: git-safe-change
description: >-
  Bezpečný postup pro každou změnu v git repozitáři s kódem — vlastní větev, viditelný
  diff, pull request, žádné destruktivní příkazy bez varování.
  Use when: uživatel chce upravit kód v repozitáři, připravit commit, otevřít pull request,
  nebo řekne "uprav X a připrav PR", "commitni to", "pushni to", "udělej z toho PR",
  "commit this", "open a pull request", "push the change".
  Použij i tehdy, když se chystáš sáhnout na kód a uživatel o gitu vůbec nemluvil.
---

# Git safe change

Cíl je jednoduchý: **žádná změna v kódu bez větve, bez diffu a bez pull requestu.** Ne proto, že by to tak bylo správně obecně, ale protože jinak se špatná změna pozná pozdě a nejde jednoduše vzít zpět.

## Kde tenhle postup platí a kde ne

| Platí | Neplatí |
|---|---|
| repozitáře se skutečným kódem a buildem | znalostní obsah PACTu — poznámky, kontext, projektová dokumentace |
| projekty typu `dual-root` a jejich kódový root | denní úklid a zálohy |
| cokoli, co se nasazuje nebo publikuje | |

U znalostního obsahu se dlouhodobě commituje přímo do hlavní větve. Je to vědomé rozhodnutí, ne nedbalost: u poznámek nemá pull request co recenzovat a jen zpomaluje.

**Když si nejsi jistý, do které kategorie věc spadá, zeptej se.** Přísnější postup u poznámek jen otravuje; volnější postup u kódu je riziko.

## Postup

1. **Zjisti stav repozitáře** — na jaké jsi větvi, jsou tam necommitnuté změny, nepushnuté commity? **Nahlas to uživateli dřív, než na cokoli sáhneš.** Cizí rozdělaná práce je nejčastější příčina toho, že se něco ztratí.
2. **Stáhni aktuální stav** výchozí větve.
3. **Založ novou větev** pojmenovanou podle úkolu, kebab-case. Podle úkolu, ne podle člověka.
4. **Udělej nejmenší změnu, která úkol splní.** Nerefaktoruj nesouvisející kód, i když tě to svrbí. Změna, která dělá dvě věci najednou, se špatně recenzuje a špatně vrací.
5. **Ukaž diff** a shrň ho lidsky: co se změnilo a proč.
6. **Commitni až po souhlasu uživatele.** Zpráva má vysvětlit změnu někomu, kdo ji bude číst za týden — ne popsat, které řádky se změnily.
7. **Pushni větev a otevři pull request** se třemi částmi: co se změnilo, proč, a jak si to ověřit.

## Tvrdá pravidla

- **Nikdy nepushuj přímo do hlavní větve.**
- **Nikdy nepoužívej force push.**
- Když se zdá, že je potřeba destruktivní příkaz — `reset --hard`, přepis historie, smazání větve se změnami — **zastav se a vysvětli riziko.** Nespouštěj to sám.
- Když se v diffu objeví `.env` nebo cokoli, co vypadá jako klíč, token nebo heslo, **zastav se a varuj.** Tajemství v historii gitu se odstraňuje mnohem hůř, než se tam dostane.

## Když nedosáhneš na repozitář

U projektu typu `dual-root` leží kód mimo PACT a agent na něj nemusí vidět.

**Neodhaduj obsah souborů podle názvu a nedomýšlej, co v nich je.** Řekni to uživateli a navrhni, jak si dosah rozšířit — způsob závisí na prostředí, ve kterém běžíš (víceklořenový workspace, přidání adresáře do relace, otevření druhého okna). Cestu ke kódu najdeš v `0_Projects/<projekt>/PROJECT.md`.

## Příklad

**Uživatel:** „Oprav mi překlep na hlavní stránce a pushni to."

**Průběh:**

```
Stav repa: větev main, čisté, 0 nepushnutých commitů. Stahuju.

Zakládám větev fix-typo-homepage.

Diff — jeden soubor, jeden řádek:
  - <h1>Vítejte na strákách</h1>
  + <h1>Vítejte na stránkách</h1>

Je to jen ten překlep, nic dalšího jsem nezměnil. Můžu commitnout?
```

*Po souhlasu:* commit `Opravit překlep v nadpisu hlavní stránky`, push větve, PR s popisem co / proč / jak ověřit.

Všimni si, co se **nestalo**: nepushlo se do `main`, i když uživatel řekl „pushni to". Formulace uživatele není pokyn obejít postup.
