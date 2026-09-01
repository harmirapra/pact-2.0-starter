---
name: pact-setup
description: >-
  Provede nového uživatele prvním nastavením PACT — preflight a devět kroků
  od identity přes git zálohu až po první dovednost a první projekt.
  Use when: uživatel řekne "pomoz mi nastavit tento pact", "použij dovednost
  pact-setup", "nastav mi PACT", "chci začít s PACTem", "projdi mě
  onboardingem", "set up PACT", "first-time setup", "onboard me", "initialize
  PACT", nebo otevře čerstvě naklonovaný PACT poprvé a neví, kde začít. Použij
  i tehdy, když `pact doctor` hlásí placeholdery a uživatel se ptá, co s tím.
---

# pact-setup

Preflight a devět kroků, jedno posezení. Cíl není vyplnit každé pole dokonale — cíl je mít po dokončení PACT, který **umí být užitečný hned**, a vědět, co ještě čeká na doplnění.

**Pravidlo pro celý průchod:** nikdy nevymýšlej odpověď za uživatele. Placeholder `[DOPLNIT]`, který zůstane placeholderem o krok déle, je lepší než vymyšlený obsah — to platí i uprostřed wizardu, ne jen mimo něj (3.1). Když uživatel na otázku nemá teď odpověď, zapiš `[DOPLNIT]` a jdi dál; wizard se dá spustit znovu.

Po každém kroku krátce shrň, co se zapsalo, a zeptej se, jestli pokračovat.

## Tón

Mluv méně formálně: krátké věty, přímé oslovení, žádné úřední obraty. Když není zřejmé, proč se na něco ptáš, stručně to vysvětli. Po dokončeném kroku můžeš jednou větou ocenit posun, ale nechval každou odpověď.

Nepřeháněj to: žádné emoji, nadšené výkřiky typu „skvělá volba!", ukecanost ani chvála po každé odpovědi. Uživatel si přišel PACT nastavit, ne si popovídat. Jazyk se řídí uživatelem.

Jakmile dokončíš krok s tone-of-voice, řiď se dál tím, co uživatel právě napsal — od té chvíle už jeho styl v repu je.

## Preflight (krok 0)

Zjisti, s čím pracuješ, dřív než začneš cokoli zapisovat:

- je nainstalovaný `git`? Ohlas stav; bez něj nepůjdou lokální gitové kroky ani záloha.
- je nainstalovaný a přihlášený `gh` (GitHub CLI)? Ohlas stav; bez něj se repo v kroku 4 založí ručně přes web.
- je dostupný `python3 3_Tools/bin/pact --help`? Pokud ne, zastav se — bez CLI nejde ověřit žádný další krok.
- ve kterém coding agentovi právě běžíš? Zapiš si jeho jméno pro krok 5 — půjde do `stack.md`.

`git` a `gh` jsou doporučené, ne povinné. Co chybí, zmiň i s dopadem a
pokračuj; na chybějícím `gh` nikdy nekonči.

## Krok 1 — Kdo jsi → `2_Context/identity/about-me.md`

**Nejdřív zkontroluj existující identitu, ne až když na ni narazíš náhodou.** Uživatelská úroveň — soubor napsaný přímo uživatelem, ne vygenerovaný (např. `~/.claude/CLAUDE.md` u Claude Code, nebo obdobný soubor jiného nástroje) — je načtená pořád, je to jistota prostředí, ne výjimka. Než se začneš ptát od nuly:

1. Podívej se, jestli takový uživatelem psaný soubor existuje (u Claude Code typicky `~/.claude/CLAUDE.md`; jiné nástroje mají vlastní ekvivalent).
2. Pokud ano, **ukaž jeho obsah**, navrhni, jak by z něj vycházel `about-me.md`, a **počkej na výslovné potvrzení** — nezapisuj sám, ani po částech.
3. Pokud uživatel odmítne, nebo takový soubor neexistuje, jdi klasickou cestou: otevři soubor, projdi placeholdery po sekcích (Kdo jsem / Co dělám / Jak se mnou mluvit / Co má agent vědět, aby neplýtval časem) a ptej se po jedné sekci, ne na všechno najednou.
4. Ať zápis vznikl importem nebo rozhovorem, přidej na konec souboru poznámku o zdroji (např. *„převzato z uživatelského souboru nástroje [jméno], potvrzeno uživatelem [datum]"* nebo *„napsáno v rozhovoru [datum]"*) — za měsíc musí jít poznat, co je čí.

**Tvrdý zákaz zdroje:** `~/.claude/rules/`, `~/.copilot/instructions/`, `~/.agents/skills/` a obdobné cesty **nikdy** nejsou zdroj pro import. Jsou to artefakty vygenerované `pact sync` — čerpat z nich do kanonického zdroje je kruhové a porušuje princip P1 (jeden kanonický zdroj, generované adaptéry). Zdrojem smí být jen soubor, který napsal přímo uživatel.

Připomeň před zápisem: tenhle soubor zůstává jen v PACTu. `pact sync` ho
neinstaluje do konfiguračních cest agentů; kdo ho tam chce mít, zkopíruje si
ho ručně sám.

## Krok 2 — Jak píšeš → `2_Context/identity/tone-of-voice/`

Stejně jako v kroku 1: pokud existuje uživatelem psaný soubor na uživatelské úrovni, ze kterého jde styl vytěžit, nabídni import, ukaž návrh a počkej na potvrzení — nikdy nečerpej z `~/.claude/rules/`, `~/.copilot/instructions/` ani obdobných generovaných cest (stejný zákaz jako v kroku 1).

Jinak je nejpřesnější cesta dovednost `personal-voice-analyst` — z reálných textů pozná styl líp, než ho uživatel sám popíše. Nabídni ji: *„Mám vytáhnout styl z tvých textů, nebo ho popíšeš rovnou?"*

Když textů nemá dost (`personal-voice-analyst` řekne, jestli vzorek stačí), doplň sekce ručně stejně jako u kroku 1. Zápis vždy doplň poznámkou o zdroji (import / analýza textů / rozhovor).

**Podotázka ke kvalitě výstupu (rozhodnutí O-A, S1):** zeptej se rovnou i na `2_Context/quality-criteria.md` — soubor, který čte dovednost `quality-gate`. Otázka: *„Podle čeho poznáš, že je text nebo výstup dost dobrý? Klidně jen pár vět — cokoli je lepší než nic."* Není to nový krok navíc, je to sesterský soubor tone-of-voice — obojí čte stejná dovednost (`quality-gate`) předtím, než něco schválí.

## Krok 3 — Cíle → `2_Context/goals/goals.md`

Krátký horizont stačí — čtvrtletí, ne pětiletý plán. Ptej se: *co teď řešíš, co by ses rád naučil, čemu se chceš vyhnout.* Připomeň, že `goals.md` zůstává jen v PACT — na rozdíl od kroku 1 tu není co ani nabízet ke kopírování ven, cíle nemají co dělat nad cizím kódem.

## Krok 4 — Git, GitHub, záloha

Wizard git **nespouští** — jen vypíše příkazy, vysvětlí, co dělají, a spuštění nechá na uživateli (stejný princip jako u kroku, který dřív zapisoval do `$HOME`: schopnost commitovat nebo pushovat za uživatele wizard nemá mít, ne jen zákaz).

1. Pokud repo ještě nemá `.git`: ukaž příkaz `git init` a založení větve `main`, vysvětli k čemu je.
2. Nech uživatele potvrdit jméno repa. Neodvozuj ho z účtu ani ze jména složky.
3. Pokud je `gh` dostupný a přihlášený: ukaž `gh repo create <potvrzené-jméno> --private --source=.`. Tenhle příkaz selže, pokud repo stejného jména už existuje; žádnou URL neodhaduj.
4. Pokud `gh` chybí: vypiš kroky k ručnímu založení private repa na GitHubu. Uživatel pak nadiktuje přesnou URL; nikdy ji nedoplňuj ani neodhaduj.
5. Ukaž příkaz na první commit a push a vysvětli, že je to záloha. **Nespouštěj ho** — uživatel ho spustí sám, až bude chtít.

Bez tohohle kroku nemá `pact doctor` co kontrolovat u „nepushnuté commity" a `daily-tidy` nemá kam zálohovat — ale iniciativu ke commitu a pushi má mít vždy uživatel, ne wizard (viz meze v `docs/ARCHITECTURE.md`: co agent udělá s gitem mimo tenhle krok, PACT neovlivní).

## Krok 5 — Stack a vrstvy → `2_Context/stack.md`

Vysvětli tři vrstvy schopností (`docs/VRSTVY.md`): PACT (dovednosti + kontext, přenositelné) / rozšíření agenta (pluginy, hooks, slash commands — vendor-specific) / externí nástroje (MCP, API).

Zeptej se, jaké agenty a rozšíření uživatel používá (z kroku 0 už znáš jednoho). Zapiš do `stack.md` — je to jen záznam, `pact-setup` nic z vrstvy 2 neinstaluje (3.9: *wizard neinstaluje, vysvětlí a zaznamená*). Pokud něco z vrstvy 2 pokrývá stejné území jako baseline dovednost v `1_Abilities/skills/`, zapiš to jako kandidáta pro `plugin-collision-review`, nerozhoduj to tady.

## Krok 6 — Tajemství

1. Ověř, že `.env` je v `.gitignore` (má být od začátku).
2. Pokud uživatel má API klíče, ukaž `.env.example` a vysvětli, že hodnoty patří do `.env`, nikdy do trackovaného souboru.
3. Spusť kontrolu tajemství (`pact doctor`, řádek se sekcí "tajemství") a ukaž výsledek.
4. Zmiň dovednost `git-safe-change` — bude ji používat u každé budoucí změny v kódovém repu.

## Krok 7 — První dovednost

Projdi `1_Abilities/REGISTRY.md` s uživatelem. U dovedností, které ho zajímají, **otevři jejich `description` a dopiš spouštěcí frázi, kterou by sám použil** — návazek ze zastávky S2: popisy v šabloně jsou obecné záměrně, protože šablona neví, kdo ji naklonuje; tenhle krok je jediná chvíle, kdy se na popis podívá dřív, než ho začne zlobit, že se dovednost nespustila.

Nemusí projít všech deset — stačí ty, u kterých pozná, že by je použil brzy.

## Krok 8 — První projekt

Spusť `python3 3_Tools/bin/pact new <nazev>` interaktivně a nech rozhodovací otázku položit CLI — její znění je závazné. Pokud se uživatel zeptá na rozdíl mezi `single-root` a `dual-root`, cituj sekce „Rozhodovací otázka" a „Dva typy" z `docs/DUAL-ROOT.md`; neparafrázuj je a nepřidávej vlastní doporučení, který typ je lepší nebo běžnější.

U `dual-root` pokračuj takto:

1. `pact new` položí rozhodovací otázku; ty ji nekomentuj ani nepředjímej.
2. Nech uživatele potvrdit cestu ke kódu.
3. Pokud adresář neexistuje, smíš ho založit.
4. Vypiš nejdřív `cd <potvrzená-cesta>` a teprve pak `git init` a případné
   `gh repo create <potvrzené-jméno> --private --source=.` z kroku 4. Příkazy
   nespouštěj — provede je uživatel.
5. Až je repo hotové, spusť `pact link`; to je operace uvnitř PACTu a obsluhuje ji agent.

## Krok 9 — `pact doctor` — verifikace

Spusť `python3 3_Tools/bin/pact doctor` a projdi výstup řádek po řádku s uživatelem. Na čerstvé instanci je normální vidět několik `WARN` (placeholdery, které z wizardu vypadly, nepushnuté commity) — to není chyba, je to seznam toho, co zbývá. `FAIL` naopak znamená, že je něco rozbité a wizard sám o sobě neskončil úspěšně; zastav se a najdi příčinu, ne pokračuj dál.

Na konci shrň: co je hotové, co zůstalo jako `[DOPLNIT]`, a že `daily-tidy`
odteď dělá pravidelnou kontrolu za uživatele. Připomeň, že se může kdykoli
zeptat: *„pověz mi, jak používat tento pact"*.
