---
name: rpi-implement
description: >-
  Třetí fáze RPI (Research → Plan → Implement → Review) — provede hotový
  plán krok za krokem a zapíše, co se skutečně změnilo.
  Use when: uživatel řekne "implementuj ten plán", "rozjeď implementaci",
  "rpi implement", "execute the plan", "start implementing", nebo odevzdá
  hotový `*-plan.md` a chce pokračovat další fází RPI.
---

# RPI — Implement

Tohle je jediná fáze RPI, která **smí psát a upravovat kód** — a taky jediná, která se odehrává v kódovém repu, ne v PACT (viz `docs/DUAL-ROOT.md` u projektů typu `dual-root`).

## Vstup

Přečti `*-plan.md` **jako soubor**. Pokud plán chybí, je neúplný, nebo některý krok nejde provést tak, jak je napsaný, **zastav se a řekni to** — needomýšlej, co plán „asi myslel". Rozpor mezi plánem a skutečností je nález, ne překážka k obejití.

## Postup

1. Projdi kroky **v pořadí ze závislostí**, ne v pořadí, které se ti zdá rychlejší.
2. U každého kroku: proveď přesně to, co říká. Když cestou zjistíš, že je potřeba víc, než plán čekal, zaznamenej to jako odchylku — nerozšiřuj krok mlčky.
3. Po každém kroku odškrtni ho v `*-plan.md` (nebo v kopii, kterou pak uložíš jako changes).
4. Neprováděj nic, co v plánu není — ani „drobné vylepšení, když už jsem tady". To je práce pro jiný úkol nebo pro `git-safe-change`, ne pro tenhle krok.

## Výstup

Kód + `0_Projects/<projekt>/rpi/RRRR-MM-DD-<téma>-changes.md`:

```markdown
# Changes: <téma>

Vychází z: RRRR-MM-DD-<téma>-plan.md

## Provedené kroky
- [x] 1. <co se udělalo> — commit/diff odkaz
- [x] 2. ...

## Odchylky od plánu
- krok 3: plán čekal X, skutečnost byla Y, protože ...

## Co zůstalo neudělané
- <krok> — <proč>
```

Samotná změna v kódu jde přes `git-safe-change` (větev, diff, PR) — RPI implementaci neobchází, jen ji předchází researchem a plánem.

## Kritické pravidlo: vyčisti kontext před další fází

Fáze Review dostane `*-plan.md` a `*-changes.md` jako soubory, ne tuhle konverzaci. Nová konverzace nebo `/clear`. Review, které vzniklo ve stejné konverzaci jako implementace, má sklon potvrdit vlastní práci místo aby ji nezávisle prověřilo.
