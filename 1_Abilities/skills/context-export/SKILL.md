---
name: context-export
description: >-
  Týdenní kontrola, jestli v konverzacích s agentem vzniklo něco trvalého,
  co ještě nezapsané v PACT.
  Use when: uživatel řekne "co jsem se tenhle týden dozvěděl", "context
  export", "zkontroluj, jestli mi něco neuteklo z konverzací", "shrň, co
  má jít do PACT", "weekly context check", "did anything need to be saved",
  nebo si všimne, že se stejnou věc vysvětluje agentovi podruhé.
---

# context-export

**Princip, na kterém tahle dovednost stojí (P10):** paměť nástroje — historie konverzací, paměť Claude Desktopu, project knowledge — **není kanonický kontext, je to cache.** Co v ní zůstane a nikam jinam se nezapíše, je ztracené v okamžiku, kdy se cache smaže, obmění nebo přejde se na jiný nástroj.

**Cíl není synchronizovat paměť nástroje automaticky — cíl je, aby na ní nezáleželo.**

## Postup

1. Zeptej se přímo: *„Vzniklo v posledních konverzacích něco, co by se mělo pamatovat trvale — rozhodnutí, preference, fakt o projektu, něco, co jsi mi vysvětloval a nechceš to vysvětlovat znovu?"*
2. Pro každou takovou věc rozhodni, kam patří:

| Co to je | Kam |
|---|---|
| trvalý fakt o uživateli, jeho stylu nebo cílech | `2_Context/identity/` nebo `goals/goals.md` |
| doménová znalost, terminologie | `2_Context/expertise/` |
| rozhodnutí nebo poznatek vázaný na konkrétní projekt | `0_Projects/<projekt>/architecture.md` nebo `PRD.md` |
| opakující se postup, který ještě není dovednost | zvaž `skill-builder` (pravidlo eskalace — potřetí) |

3. Zapiš to tam, ne do nového souboru navíc — nejdřív zkontroluj, jestli už existuje vhodné místo.
4. Když si nejsi jistý, jestli věc je „trvalá", nebo jen aktuální kontext jedné úlohy, **zeptej se uživatele**. Neukládej automaticky všechno — `2_Context/` má zůstat čitelný, ne se stát druhým chatlogem.

## Kdy tuhle dovednost spustit

Týdně, nebo kdykoli si uživatel všimne, že agentovi něco vysvětluje podruhé — to je nejspolehlivější signál, že něco chybí v `2_Context/`, ne v paměti nástroje.

## Co dělat, když se najde hodně najednou

Neukládej všechno jedním zápisem bez rozmyslu. Seřaď podle toho, co bude nejdřív chybět, a projdi to s uživatelem po jednom — je to totéž pravidlo jako u `pact-setup`: raději méně a rozhodnuto, než hodně a domyšleno za uživatele.
