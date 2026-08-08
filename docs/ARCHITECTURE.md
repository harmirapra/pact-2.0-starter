# Architektura

Destilát rozhodovacího dokumentu (`PACT-klon_cilovy-stav-a-plan.md`, v3.2) pro čtenáře tohoto repozitáře. Kde se tenhle text a rozhodovací dokument rozejdou, platí rozhodovací dokument — tenhle soubor je shrnutí, ne nový zdroj pravdy.

## Proč PACT-2.0 existuje

PACT-2.0 je výchozí šablona pro nové instance frameworku **PACT** (Projects · Abilities · Context · Tools), postavená na třech požadavcích:

- **Vendor neutralita** — instance musí fungovat i tam, kde konkrétní coding agent není k dispozici (horizont: bankovní prostředí s GitHub Copilotem).
- **Dual root** — kontext a kód mají odlišný životní cyklus (pomalý a lidský vs. rychlý a strojový) a nesdílejí historii.
- **Neutrální jádro + generované adaptéry** — kanonický zdroj je jeden a nezávislý na nástroji; `.claude/`, `.github/`, `.agents/` a instalace do `$HOME` jsou z něj *generované* build artefakty, nikdy ručně editovaná pravda.

## Principy

| # | Princip | Důsledek |
|---|---|---|
| P1 | Jeden kanonický zdroj, generované adaptéry | `.claude/`, `.github/`, `.agents/`, `$HOME` — nikdy needituj ručně |
| P2 | Standard před vlastním řešením | `AGENTS.md` + `SKILL.md`, otevřené standardy |
| P3 | Routing je data, ne tabulka | dovednost se aktivuje přes `description`, ne přes seznam v instrukčním souboru |
| P4 | Kontext a kód mají oddělenou historii | dual root — nezávisle na viditelnosti repozitáře |
| P5 | Vstupní bod je vždy PACT | nikdy neotvírej kódové repo jako výchozí pracoviště |
| P6 | Kódové repo je čistě kódové | dovednosti a kontext přicházejí z PACT |
| P7 | Kontext se dělí podle stability, ne podle projektu | tři úrovně rozsahu (`docs/ROZSAH-KONTEXTU.md`) |
| P8 | Deklarace místo objevování | projekt vyjmenuje, co potřebuje, agent nehádá |
| P9 | Ostrá hranice distribuovatelné / osobní | `1_Abilities/`, `AGENTS.md` vs. `2_Context/`, `0_Projects/` |
| P10 | PACT je jediný kanonický kontext | paměť nástroje je cache, ne pravda (`context-export`) |
| P11 | Co se neverzuje, neexistuje | každá změna kontextu končí commitem |
| P12 | Kontext se dodává nezávisle na mechanismu | pravidla do `AGENTS.md`, ne do jednotlivé dovednosti (`docs/VRSTVY.md`) |
| P13 | PACT musí být soběstačný při iniciaci | baseline dovednosti zůstávají i tam, kde by je jinak nahradilo rozšíření agenta |

## Struktura repozitáře

Čtyři pilíře (`AGENTS.md`):

| Složka | Otázka | Obsah |
|---|---|---|
| `0_Projects/` | CO dělám? | znalostní část projektů, šablona `_TEMPLATE/` |
| `1_Abilities/` | JAK to dělat? | dovednosti — `SKILL.md`, otevřený standard |
| `2_Context/` | KDO jsem / co dělám? | identita, tone of voice, cíle, expertiza, `scope.yml`, `stack.md` |
| `3_Tools/` | S ČÍM? | CLI `pact`, testy |

Generované a negitignorované (`.agents/`, `.claude/`, `.github/`) se necommitují — vyrábí je `pact sync` z kanonického zdroje.

## Klíčová rozhodnutí

**Neutrální jádro + generované adaptéry (R2).** Kdyby „neutrální" znamenalo nejmenší společný jmenovatel, ztratí se to nejlepší z každého nástroje. Řešením je generovat nativní strukturu pro každého, ne ji zakazovat.

**Tři úrovně rozsahu kontextu (R3).** Instrukční soubory kaskádují nahoru stromem, dovednosti ne — hledají se jen v definovaných adresářích. Práce v podsložce bez otevřeného PACT rootu proto tiše ztrácí dovednosti. Řeší se rozsahem (uživatelská/repo/podsložka úroveň), ne disciplínou. Podrobně `docs/ROZSAH-KONTEXTU.md`.

**Dva typy projektů, otočená rozhodovací otázka.** Místo předvídání („vznikne tu kód s vlastním životním cyklem?") se `pact new` ptá na to, co uživatel v okamžiku zakládání skutečně ví: bude mít projekt vlastní repozitář vedle PACTu, nebo zůstane celý uvnitř? Viditelnost je spolehlivý *ukazatel* na jiný životní cyklus, ne jeho *příčina* — dva rooty existují kvůli tempu změn, ne kvůli tomu, jestli je něco veřejné. Podrobně `docs/DUAL-ROOT.md`.

**`pact doctor`: `WARN` ≠ `FAIL`.** Šablona, jejíž hodnotou je onboarding, nemá první příkaz po `git clone` vítat hlášením o selhání. Rozlišovací princip: `WARN` = ještě nenastaveno nebo vědomě odložené (placeholdery, nezacommitované změny, `$HOME` neodpovídá zdroji), `FAIL` = skutečně rozbité nebo nekonzistentní (tajemství, nevalidní frontmatter, rozjeté adaptéry, mrtvý odkaz).

**Triáž dovedností podle jiného kritéria než „co používám".** Šablona se neptá, co konkrétní člověk za měsíc použil — ptá se, co potřebuje cizí čerstvá instance první den, aby byla soběstačná (princip P13). Výsledek: 18 dovedností — 9 baseline z pact-starteru, 1 sklizeň z existující instance (`git-safe-change`), 4 wizard/údržba, 4 RPI. Kompletní přehled i s odůvodněním v `1_Abilities/REGISTRY.md` a v pracovních souborech review.

**Routing je data, a data se ladí (P3).** Pole `description` v každém `SKILL.md` rozhoduje, kdy se dovednost aktivuje — ale popisy v týhle šabloně jsou psané **obecně a záměrně nevyladěné**. Šablona neví, kdo ji naklonuje, jakým jazykem mluví nebo jakou frází si o věc řekne, takže spouštěcí fráze v `description` jsou nutně kompromis, ne finální stav. `pact-setup` (krok 8) proto vede nového uživatele k tomu, aby si u dovedností, které ho zajímají, popis rovnou doladil na vlastní slovník — a `scope-review` později kontroluje, jestli dovednost, která nikdy nevystřelila, nemá problém v obsahu, nebo jen ve špatně trefeném popisu. Routing se nekazí jednou při stavbě šablony; udržuje se průběžně.

## RPI — tři poznámky

Čtyři dovednosti (`rpi-research`, `rpi-plan`, `rpi-implement`, `rpi-review`) jsou adaptací metodiky Research → Plan → Implement → Review, zdokumentované v `microsoft/hve-core`. Tři věci, které je potřeba přiznat na rovinu:

**(a) V praxi neověřené.** Na rozdíl od ostatních dovedností v šabloně, které někdo skutečně používal, je tohle adaptace cizí metodiky bez reálného provozu v PACT-2.0. Je to první kandidát na revizi, jakmile projde prvním skutečným použitím.

**(b) Zákaz psát kód ve fázích Research a Plan stojí na instrukci, ne na omezení nástrojů.** hve-core ho vynucuje přes `tools:` frontmatter u Copilot agenta — mechanismus vázaný na jeden nástroj, který neutrální dovednost nemá k dispozici. Je to vědomě slabší záruka: dovednost agentovi *řekne*, že v týhle fázi nesmí psát kód, ale nemá jak mu to fyzicky zabránit. **Když zjistíš, že agent tohle pravidlo nedrží** (píše kód i ve fázi Research nebo Plan), nejde o chybu k tichému přehlédnutí — uprav zadání pro danou fázi tak, aby to bylo nepřehlédnutelné, nebo fázi zopakuj v čistší konverzaci. Spoléhat na to, že si agent pravidlo příště lépe pohlídá sám, metodu neopraví.

**(c) Vyčištění kontextu mezi fázemi je nejkřehčí článek celé metody.** Je to jediný krok, který nezajistí ani agent (nemá důvod sám ukončit konverzaci), ani `AGENTS.md` (může jen připomenout, ne vynutit). Když ho uživatel vynechá, RPI degraduje zpátky na řetěz promptů v jedné konverzaci — tedy přesně na to, co nahrazovalo staré `RECIPES.md` z pact-starteru — a většina přínosu (nezávislé ověření každé fáze) zmizí. Každá ze čtyř dovedností na to proto upozorňuje samostatně, ne jen jednou v `AGENTS.md`.

## Zvážené a vědomě nepostavené

**`daily-git-sync`** — skript pro automatický commit a push, doložený jako path-agnostický nástroj v existující instanci, ze které šablona čerpala jako zdrojový materiál (naplňuje požadavek na git a zálohování, viz `docs/DUAL-ROOT.md` a princip P11). Do PACT-2.0 se **vědomě nepřenesl**: žádná fáze F0–F7 ho nezmiňuje, je to rozšíření rozsahu, ne položka triáže, a automatický commit + push na cizím stroji je riziko, u kterého se chyba pozná pozdě. `daily-tidy` (`1_Abilities/skills/daily-tidy/`) dělá totéž vědomě a na vyzvání uživatele, ne automaticky na pozadí. Je to kandidát na doplnění, ne zapomenutá položka — pokud budoucí revize dojde k tomu, že riziko stojí za to, `daily-git-sync` je hotový vzor, ze kterého se dá vyjít.

## Vědomá omezení

| Omezení | Proč |
|---|---|
| Kódové repo u `dual-root` projektů není samostatně soběstačné | dovednosti a kontext přicházejí jen z PACT (P6) |
| Uživatelská úroveň v `$HOME` není verzovaná | kanonický originál je vždy v PACT (P1, P11); na novém stroji je potřeba `pact sync` |
| Runtime arbitráž mezi dovednostmi a rozšířeními agenta není řiditelná | `SKILL.md` nemá pole pro prioritu; řeší se přes `AGENTS.md` a `scope-review`, ne za běhu (`docs/VRSTVY.md`) |
| Custom agents (`.agent.md`, subagenti) nejsou součástí v1 | nejsou přenositelné mezi nástroji |
| Distribuce pro tým (kolekce, maturity) není postavená | PACT-2.0 je zatím jednouživatelský; hranice distribuovatelné/osobní (P9) je připravená na pozdější rozšíření |
| Evals a metriky kvality dovedností nejsou součástí | vědomě mimo rozsah v1 |
| `doctor`, kontrola placeholderů: `OK` neznamená „nastaveno správně" | kontroluje jen nepřítomnost řetězce `[DOPLNIT` — nerozliší obsah napsaný uživatelem od obsahu vymyšleného agentem, a strojově to nejspíš ani nejde (nález N-4, UAT běh 1). `OK` je důkaz nepřítomnosti placeholderů, nic víc. |

## Zdroje

- [nowork-ai/pact-starter](https://github.com/nowork-ai/pact-starter) — původní framework
- [microsoft/hve-core](https://github.com/microsoft/hve-core) — zdroj metodiky RPI
- [Agent Skills — agentskills.io](https://agentskills.io/home) — standard `SKILL.md`
- [AGENTS.md spec](https://www.morphllm.com/agents-md-guide)
