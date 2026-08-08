---
name: pact-setup
description: >-
  Provede nového uživatele prvním nastavením PACT — deset kroků od identity
  přes git zálohu a rozsah kontextu až po první dovednost a první projekt.
  Use when: uživatel řekne "použij dovednost pact-setup", "nastav mi PACT",
  "chci začít s PACTem", "projdi mě onboardingem", "set up PACT", "first-time
  setup", "onboard me", "initialize PACT", nebo otevře čerstvě naklonovaný
  PACT poprvé a neví, kde začít. Použij i tehdy, když `pact doctor` hlásí
  placeholdery a uživatel se ptá, co s tím.
---

# pact-setup

Deset kroků, jedno posezení. Cíl není vyplnit každé pole dokonale — cíl je mít po dokončení PACT, který **umí být užitečný hned**, a vědět, co ještě čeká na doplnění.

**Pravidlo pro celý průchod:** nikdy nevymýšlej odpověď za uživatele. Placeholder `[DOPLNIT]`, který zůstane placeholderem o krok déle, je lepší než vymyšlený obsah — to platí i uprostřed wizardu, ne jen mimo něj (3.1). Když uživatel na otázku nemá teď odpověď, zapiš `[DOPLNIT]` a jdi dál; wizard se dá spustit znovu.

Po každém kroku krátce shrň, co se zapsalo, a zeptej se, jestli pokračovat.

## Krok 0 — Preflight

Zjisti, s čím pracuješ, dřív než začneš cokoli zapisovat:

- je nainstalovaný `git`? Bez něj nejde krok 4.
- je nainstalovaný a přihlášený `gh` (GitHub CLI)? Bez něj krok 4 založí repo ručně přes web.
- je dostupný `python3 3_Tools/bin/pact --help`? Pokud ne, zastav se — bez CLI nejde ověřit žádný další krok.
- ve kterém coding agentovi právě běžíš? Zapiš si jeho jméno pro krok 6 — půjde do `stack.md`.

Chybějící `git` nebo `gh` není důvod končit — je to WARN, pokračuj a připomeň to u kroku 4.

## Krok 1 — Kdo jsi → `2_Context/identity/about-me.md`

**Nejdřív zkontroluj existující identitu, ne až když na ni narazíš náhodou.** Uživatelská úroveň (`~/.claude/CLAUDE.md` a obdobné uživatelem psané soubory) je načtená pořád — je to jistota prostředí, ne výjimka. Než se začneš ptát od nuly:

1. Podívej se, jestli existuje soubor jako `~/.claude/CLAUDE.md` — psaný uživatelem, ne vygenerovaný.
2. Pokud ano, **ukaž jeho obsah**, navrhni, jak by z něj vycházel `about-me.md`, a **počkej na výslovné potvrzení** — nezapisuj sám, ani po částech.
3. Pokud uživatel odmítne, nebo takový soubor neexistuje, jdi klasickou cestou: otevři soubor, projdi placeholdery po sekcích (Kdo jsem / Co dělám / Jak se mnou mluvit / Co má agent vědět, aby neplýtval časem) a ptej se po jedné sekci, ne na všechno najednou.
4. Ať zápis vznikl importem nebo rozhovorem, přidej na konec souboru poznámku o zdroji (např. *„převzato z `~/.claude/CLAUDE.md`, potvrzeno uživatelem [datum]"* nebo *„napsáno v rozhovoru [datum]"*) — za měsíc musí jít poznat, co je čí.

**Tvrdý zákaz zdroje:** `~/.claude/rules/`, `~/.copilot/instructions/`, `~/.agents/skills/` a obdobné cesty **nikdy** nejsou zdroj pro import. Jsou to artefakty vygenerované `pact sync` — čerpat z nich do kanonického zdroje je kruhové a porušuje princip P1 (jeden kanonický zdroj, generované adaptéry). Zdrojem smí být jen soubor, který napsal přímo uživatel.

Připomeň před zápisem: tenhle soubor se instaluje i na uživatelskou úroveň (krok 5) — uvidí ho agent i při práci nad cizím kódem. Kontrolní otázka u citlivějších vět: *chceš, aby tohle agent viděl i mimo PACT?*

## Krok 2 — Jak píšeš → `2_Context/identity/tone-of-voice/`

Stejně jako v kroku 1: pokud existuje uživatelem psaný soubor na uživatelské úrovni, ze kterého jde styl vytěžit, nabídni import, ukaž návrh a počkej na potvrzení — nikdy nečerpej z `~/.claude/rules/`, `~/.copilot/instructions/` ani obdobných generovaných cest (stejný zákaz jako v kroku 1).

Jinak je nejpřesnější cesta dovednost `personal-voice-analyst` — z reálných textů pozná styl líp, než ho uživatel sám popíše. Nabídni ji: *„Mám vytáhnout styl z tvých textů, nebo ho popíšeš rovnou?"*

Když textů nemá dost (`personal-voice-analyst` řekne, jestli vzorek stačí), doplň sekce ručně stejně jako u kroku 1. Zápis vždy doplň poznámkou o zdroji (import / analýza textů / rozhovor).

**Podotázka ke kvalitě výstupu (rozhodnutí O-A, S1):** zeptej se rovnou i na `2_Context/quality-criteria.md` — soubor, který čte dovednost `quality-gate`. Otázka: *„Podle čeho poznáš, že je text nebo výstup dost dobrý? Klidně jen pár vět — cokoli je lepší než nic."* Není to nový krok navíc, je to sesterský soubor tone-of-voice — obojí čte stejná dovednost (`quality-gate`) předtím, než něco schválí.

## Krok 3 — Cíle → `2_Context/goals/goals.md`

Krátký horizont stačí — čtvrtletí, ne pětiletý plán. Ptej se: *co teď řešíš, co by ses rád naučil, čemu se chceš vyhnout.* Připomeň, že `goals.md` **nejde** na uživatelskou úroveň (na rozdíl od kroku 1) — cíle nemají co dělat nad cizím kódem.

## Krok 4 — Git, GitHub, záloha

1. Pokud repo ještě nemá `.git`, `git init`, větev `main`.
2. Pokud `gh` je dostupný a přihlášený: `gh repo create <nazev> --private`, nastav `origin`.
3. Pokud `gh` chybí: vypiš uživateli přesné kroky k ručnímu založení private repa na GitHubu a nastavení `origin`.
4. **Zeptej se, než cokoli pushneš.** První push je záloha — udělej ji na vyžádání, ne automaticky.

Bez tohohle kroku nemá `pact doctor` co kontrolovat u „nepushnuté commity" a `daily-tidy` nemá kam zálohovat.

## Krok 5 — Rozsah kontextu → instalace do `$HOME`

Vysvětli krátce tři úrovně (`docs/ROZSAH-KONTEXTU.md`, uživatelská/repo/podsložka) a ukaž aktuální `2_Context/scope.yml`. Výchozí stav šablony: identita na uživatelskou úroveň, dovednosti zatím žádné.

Zeptej se, jestli chce rozsah rozšířit už teď (obvykle ne — realokaci za provozu řeší `scope-review`, krok 5 stačí potvrdit výchozí stav).

**Než cokoli zapíšeš do `$HOME`, ukaž a počkej na potvrzení:**

1. Spusť `python3 3_Tools/bin/pact sync --dry-run` a ukaž celý výstup — konkrétní soubory a cesty pod `$HOME`, které by se zapsaly.
2. Zeptej se výslovně, jestli má zapsat naostro. Nepokračuj bez jasného "ano".
3. Teprve po potvrzení spusť `python3 3_Tools/bin/pact sync --yes` a ukaž výstup (kolik souborů se skutečně zapsalo).

`--yes` smíš použít **jedině** tady a jedině po tomhle potvrzení — je to jediné místo v celém wizardu, kde se sahá mimo repo do uživatelovy skutečné `$HOME` konfigurace. Bez potvrzení `pact sync` nové cesty v `$HOME` sám od sebe přeskočí (viz kontrakt v zadání, sekce 6) — pokud se to stane, není to chyba, jen ti chybí krok 2 výše.

## Krok 6 — Stack a vrstvy → `2_Context/stack.md`

Vysvětli tři vrstvy schopností (`docs/VRSTVY.md`): PACT (dovednosti + kontext, přenositelné) / rozšíření agenta (pluginy, hooks, slash commands — vendor-specific) / externí nástroje (MCP, API).

Zeptej se, jaké agenty a rozšíření uživatel používá (z kroku 0 už znáš jednoho). Zapiš do `stack.md` — je to jen záznam, `pact-setup` nic z vrstvy 2 neinstaluje (3.9: *wizard neinstaluje, vysvětlí a zaznamená*). Pokud něco z vrstvy 2 pokrývá stejné území jako baseline dovednost v `1_Abilities/skills/`, zapiš to jako kandidáta pro `scope-review`, nerozhoduj to tady.

## Krok 7 — Tajemství

1. Ověř, že `.env` je v `.gitignore` (má být od začátku).
2. Pokud uživatel má API klíče, ukaž `.env.example` a vysvětli, že hodnoty patří do `.env`, nikdy do trackovaného souboru.
3. Spusť kontrolu tajemství (`pact doctor`, řádek se sekcí "tajemství") a ukaž výsledek.
4. Zmiň dovednost `git-safe-change` — bude ji používat u každé budoucí změny v kódovém repu.

## Krok 8 — První dovednost

Projdi `1_Abilities/REGISTRY.md` s uživatelem. U dovedností, které ho zajímají, **otevři jejich `description` a dopiš spouštěcí frázi, kterou by sám použil** — návazek ze zastávky S2: popisy v šabloně jsou obecné záměrně, protože šablona neví, kdo ji naklonuje; tenhle krok je jediná chvíle, kdy se na popis podívá dřív, než ho začne zlobit, že se dovednost nespustila.

Nemusí projít všech deset — stačí ty, u kterých pozná, že by je použil brzy.

## Krok 9 — První projekt

Spusť `python3 3_Tools/bin/pact new <nazev>` interaktivně. Vysvětli rozdíl `single-root` / `dual-root` (`docs/DUAL-ROOT.md`) předtím, než na otázku odpoví. Pokud jde o `dual-root` a kód už existuje, nabídni rovnou `pact link`.

## Krok 10 — `pact doctor` — verifikace

Spusť `python3 3_Tools/bin/pact doctor` a projdi výstup řádek po řádku s uživatelem. Na čerstvé instanci je normální vidět několik `WARN` (placeholdery, které z wizardu vypadly, nepushnuté commity) — to není chyba, je to seznam toho, co zbývá. `FAIL` naopak znamená, že je něco rozbité a wizard sám o sobě neskončil úspěšně; zastav se a najdi příčinu, ne pokračuj dál.

Na konci shrň: co je hotové, co zůstalo jako `[DOPLNIT]`, a že `daily-tidy` odteď dělá pravidelnou kontrolu za uživatele.
