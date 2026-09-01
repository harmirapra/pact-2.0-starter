# Evoluce od pact-starteru

Čím se PACT-2.0 liší od výchozí šablony **pact-starter** (Filip Dřímalka /
nowork.ai) a — důležitější — **proč**. Není to changelog. Každý řádek
odpovídá na otázku, jaké riziko změna odstraňuje a jaký tradeoff za to
platí. Kde se tenhle text a rozhodovací dokument (`ARCHITECTURE.md`,
destilát v3.2) rozejdou, platí rozhodovací dokument.

Změny jsou seřazené podle **hloubky zásahu**, ne podle abecedy. Oprava chyby
mění chování jednoho příkazu; filosofický posun mění, co PACT vůbec je.
Čti shora dolů: každá vrstva předpokládá tu předchozí.

---

## 1 · Opravy chyb — místa, kde starter dělal špatnou věc tiše

Tady se nemění architektura, jen se opravuje konkrétní chování, které
selhávalo nenápadně: buď mlčelo, když mělo varovat, nebo hlásilo poplach,
když se nic nestalo.

| Co se změnilo | Ve starteru | V PACT-2.0 | Riziko, které to řeší |
|---|---|---|---|
| **`daily-tidy` místo automatického sync** | `daily-git-sync` commitoval a pushoval na pozadí | `daily-tidy` dělá totéž **na vyzvání**, ne automaticky | Automatický commit + push na cizím stroji je chyba, která se pozná pozdě. Explicitní vyzvání drží člověka ve smyčce. Vzor `daily-git-sync` zůstává zdokumentovaný jako kandidát, ne smazaný. |
| **`WARN` ≠ `FAIL` v `pact doctor`** | první běh po klonu mohl skončit `FAIL` na placeholderech | `WARN` = nenastaveno / vědomě odloženo · `FAIL` = rozbité (tajemství, nevalidní frontmatter, mrtvý odkaz) | Šablona, jejíž hodnotou je onboarding, nesmí prvním příkazem po `git clone` hlásit selhání, když se nic nerozbilo — jen ještě nedošlo k nastavení. Špatná zpráva o produktu, kterou by `daily-tidy` opakoval denně. |
| **Provenance jako `WARN`, ne blokace** | chybějící původ obsahu se neřešil systematicky | chybějící provenance je `WARN`; `OK` je jen důkaz **nepřítomnosti** placeholderů | `doctor` neumí odlišit text napsaný člověkem od textu vymyšleného agentem — a strojově to nejspíš nejde. Přiznaná mez místo falešné jistoty (nález N-4, UAT běh 1). |

**Společný jmenovatel:** starter volil buď mlčení (auto-sync), nebo falešný
poplach (`FAIL` na čerstvém klonu). PACT-2.0 obojí nahrazuje **kalibrovaným
signálem** — hlásí přesně tehdy, když se má rozhodovat člověk.

---

## 2 · Standardizace — vlastní formát nahrazen otevřeným standardem

Starter řešil orchestraci a routing vlastními soubory vázanými na jeden
nástroj. PACT-2.0 je nahrazuje otevřenými standardy. Motiv není estetika,
ale **trvanlivost**: formát jednoho nástroje zastará s tím nástrojem.

| Co se změnilo | Ve starteru | V PACT-2.0 | Proč standard vyhrává |
|---|---|---|---|
| **`AGENTS.md` jako jediný zdroj pravidel** | pravidla roztroušená, `CLAUDE.md` s vlastní kopií | `AGENTS.md` je kanonický; `CLAUDE.md` je jednořádkový ukazatel | Mezi-nástrojový standard, který agenti obecně respektují. Jedna kopie pravidel = žádná divergence mezi nástroji. |
| **`SKILL.md` (Agent Skills) místo ad-hoc dovedností** | dovednosti bez jednotného kontraktu | složka + `SKILL.md` s povinným `name` + `description` frontmatterem | Přenositelný standard (agentskills.io). Tentýž soubor čte Claude Code, Copilot i Cursor — **tohle je mechanismus, který enabluje agent-agnosticitu z §4.** |
| **Routing přes `description`, ne přes trigger tabulku** | `.cursorrules` — trigger mapa vázaná na Cursor | spouštěcí fráze žijí v poli `description` každého `SKILL.md` (princip P3) | „Routing je data, ne tabulka." Aktivace dovednosti cestuje s dovedností, ne v centrálním souboru jednoho nástroje. Data se navíc dají ladit (`pact-setup` krok 7, `plugin-collision-review`) — routing se udržuje průběžně, nekazí se jednou při stavbě. |

**Řetězení:** `SKILL.md` (standard) je nutná podmínka pro to, aby jedna
dovednost běžela pod libovolným agentem. Bez něj by agent-agnosticita (§4)
zůstala záměrem bez mechanismu. Standardizace tedy není samostatný cíl —
je to infrastruktura pro filosofický posun níž.

---

## 3 · Architektonické změny — jiná topologie workspace

Tady se mění samotný tvar systému: kolik má kořenů, jak se dělí kontext, jak
teče práce. Tyhle změny jsou nevratné bez přestavby a nesou největší
tradeoffy.

### 3.1 · Dual root — jádro celého rozhodnutí

Nejhlubší architektonická změna, a proto zaslouží víc než řádek. Inspirace:
**`microsoft/hve-core`**.

- **Co starter dělal:** kontext i kód v jednom repu, sdílená historie.
- **Co dělá PACT-2.0:** kontext a kód mají **oddělené kořeny** a **nesdílejí
  git historii**.
- **Proč — hlubší důvod než „přehlednost":** kontext a kód mají **odlišný
  životní cyklus**. Kontext se mění pomalu a lidsky (identita, cíle, tón);
  kód rychle a strojově. Kdyby sdílely historii, každá z nich by zašuměla tu
  druhou — commit do kódu by rozmělnil historii kontextu a naopak.
- **Co si PACT-2.0 vzal z hve-core:** oddělení **fází** práce (Research →
  Plan → Implement → Review) jako soubory na disku, ne stav chatu; agent
  s omezenými nástroji ve fázi, kde nemá psát. Cílem je **vynutit ověření**
  místo „věrohodně vypadajícího kódu". Rozhraní RPI (§3.3) kopíruje tutéž
  hranici, kterou zavádí dual root: **znalost zůstává v PACT, kód v kódovém
  repu.** Obě rozhodnutí se navzájem posilují.
- **Otočená rozhodovací otázka:** `pact new` se neptá „vznikne tu kód
  s vlastním cyklem?" (předpověď), ale „bude mít projekt vlastní repozitář
  a jakou viditelnost?" (fakt, který uživatel zná teď). Viditelnost je
  spolehlivý *ukazatel* jiného životního cyklu, ne jeho *příčina*.
- **Tradeoff, který se přiznává:** kódové repo `dual-root` projektu **není
  samostatně soběstačné** — dovednosti a kontext přicházejí jen z PACT (P6).
  Kdo otevře jen kódové repo, nemá dovednosti. Mitigace: vstupní bod je vždy
  PACT (P5). Podrobně `docs/DUAL-ROOT.md`.

### 3.2 · Tříúrovňový model rozsahu kontextu

| Aspekt | Ve starteru | V PACT-2.0 |
|---|---|---|
| Dělení kontextu | podle projektu | podle **stability** — tři úrovně rozsahu (P7) |
| Kaskádování | implicitní, nevyřčené | **explicitní model** (`docs/ROZSAH-KONTEXTU.md`) |

**Riziko, které to řeší — a proč souvisí s dual rootem:** instrukční soubory
(`AGENTS.md`, pravidla) **kaskádují nahoru** stromem adresářů, ale dovednosti
**ne** — hledají se jen v definovaných adresářích. Práce v podsložce bez
otevřeného PACT rootu proto **tiše ztrácí dovednosti**. Starter tuhle
asymetrii nikde nepojmenoval; PACT-2.0 ji dělá explicitní a **vědomě přijímá**
riziko na uživatelské úrovni (`$HOME`) místo toho, aby ho řešil instalací —
ta napáchala víc škody než užitku (`fix-brief-03.md`, nálezy N-3/N-8/N-9/N-12).
Mitigace je znovu P5. Kaskádování tedy závisí na tom, že vstupní bod je vždy
PACT — což je totéž pravidlo, které drží pohromadě dual root.

### 3.3 · RPI — pipeline místo řetězu promptů

- **Co nahrazuje:** staré `RECIPES.md` ze starteru. **Ale ne 1:1** — recept 1
  byl kódový (ten RPI nahrazuje), zbývajících 6 bylo znalostních (ty žijí dál
  jinde). RPI není náhrada celého `RECIPES.md`, jen jeho kódové části.
- **Čtyři dovednosti:** `rpi-research`, `rpi-plan`, `rpi-implement`,
  `rpi-review` — adaptace metodiky Research → Plan → Implement → Review
  z `microsoft/hve-core`.
- **Nejkřehčí článek:** vyčištění kontextu **mezi fázemi**. Nezajistí ho ani
  agent (nemá důvod sám ukončit konverzaci), ani `AGENTS.md` (umí připomenout,
  ne vynutit). Když ho uživatel vynechá, RPI **degraduje zpět na řetěz promptů
  v jedné konverzaci** — tedy přesně na to, co nahrazovalo `RECIPES.md` — a
  přínos (nezávislé ověření každé fáze) zmizí. Proto na to upozorňuje každá ze
  čtyř dovedností zvlášť, ne jen `AGENTS.md`.
- **Přiznaná slabina:** zákaz psát kód ve fázích Research/Plan stojí na
  **instrukci, ne na omezení nástrojů**. hve-core ho vynucuje přes `tools:`
  frontmatter Copilot agenta — mechanismus vázaný na jeden nástroj, který
  neutrální dovednost nemá. Vědomě slabší záruka.

### 3.4 · Integrované nástroje pro zdraví PACTu

PACT-2.0 přináší explicitní sadu nástrojů pro údržbu repozitáře — vznikly
postupně z požadavku na nezávislost na konkrétním AI agentovi a na
mechanismy, které stav repozitáře samy diagnostikují a pomáhají udržet
zdravý a zálohovaný:

| Nástroj | Typ | Co dělá |
|---|---|---|
| `pact sync` | CLI | generuje adaptéry (`.agents/`, `.claude/`, `.github/`) z kanonického zdroje |
| `pact doctor` | CLI | diagnostika stavu repozitáře — `OK`/`WARN`/`FAIL` (§ „WARN ≠ FAIL" výše) |
| `pact registry` | CLI | přegeneruje `1_Abilities/REGISTRY.md`, drží přehled dovedností aktuální |
| `daily-tidy` | dovednost | denní rutina na vyzvání: `doctor` → úklid výstupů → commit + nabídka pushe |
| `plugin-collision-review` | dovednost | detekuje kolize baseline dovedností s nainstalovanými pluginy, zapisuje rozhodnutí do `stack.md` |

Společný princip: údržba je **explicitní a na vyzvání**, ne tichá a
automatická na pozadí (viz `daily-git-sync` v sekci 1) — chyba se má poznat
hned, ne se najít o týden později.

---

## 4 · Filosofické posuny — mění se, co PACT je

Nejabstraktnější vrstva, ale řídí všechny předchozí. Tady se nemění příkaz
ani topologie, ale **cíl a hodnoty** frameworku.

### 4.1 · Agent-agnosticita: neutrální jádro + generované adaptéry

- **Posun:** starter byl de facto vázaný na jeden nástroj. PACT-2.0 stojí na
  **vendor neutralitě** — instance musí fungovat i tam, kde konkrétní coding
  agent není k dispozici (cílový horizont: bankovní prostředí s GitHub
  Copilotem).
- **Jak, aniž by se ztratilo to nejlepší z každého nástroje:** kanonický zdroj
  je jeden a neutrální; `.claude/`, `.github/`, `.agents/` jsou z něj
  **generované build artefakty** (`pact sync`), nikdy ručně editovaná pravda
  (P1). Kdyby „neutrální" znamenalo nejmenší společný jmenovatel, ztratilo by
  se to nejlepší z každého nástroje — proto se nativní struktura **generuje**,
  ne zakazuje (R2).
- **Závislost na §2:** tenhle posun je proveditelný **jen díky** `SKILL.md`
  a `AGENTS.md` z §2. Standardizace je mechanismus; agent-agnosticita je cíl,
  který ten mechanismus umožňuje. Bez otevřeného kontraktu dovednosti by
  „neutralita" zůstala prohlášením.
- **Soběstačnost při iniciaci (P13):** baseline dovednosti zůstávají i tam,
  kde by je jinak nahradilo rozšíření konkrétního agenta. Triáž se neptá „co
  jsem za měsíc použil?", ale „co potřebuje cizí čerstvá instance první den?".
  Proto testování začíná na **čerstvém klonu**, ne na autorově stroji, kde
  vznikal starter.

### 4.2 · P12 — doplňuj, nesoutěž

- **Pravidlo:** kontext se dodává **nezávisle na mechanismu**. Pravidla patří
  do `AGENTS.md`, ne do jednotlivé dovednosti (`docs/VRSTVY.md`).
- **Rozlišení, které dělá pravidlo funkčním:** **duplikace je OK, kontradikce
  ne.** Dvě místa smějí říkat totéž (redundance je odolnost); nesmějí si
  odporovat. Runtime arbitráž mezi dovednostmi a rozšířeními agenta není
  řiditelná (`SKILL.md` nemá pole pro prioritu), takže se kolize řeší
  **před během** — přes `AGENTS.md` a `plugin-collision-review`, ne za běhu.

### 4.3 · Jazyk dovednosti: mono jazyk těla, dvojjazyčná aktivace

- **Posun:** starter neřešil jazyk dovednosti jako samostatnou otázku vůbec.
  PACT-2.0 rozlišuje dvě různé věci, které se snadno slijí do jedné: jazyk,
  ve kterém je **napsané tělo** `SKILL.md`, a jazyk, ve kterém agent **vede
  interakci** po aktivaci.
- **Rozhodnutí:** tělo zůstává psané česky, jako jediný autorský zdroj — žádná
  duplicitní CZ/EN verze k údržbě. Aktivace (pole `description`) ale musí
  chytit obě jazykové varianty spouštěcí fráze (`skill-builder`, pravidlo #2).
  Jakmile se dovednost spustí, agent zbytek interakce vede v jazyce vstupu
  uživatele, ne nutně v jazyce, ve kterém je tělo napsané.
- **Proč to není totéž co P12:** P12 řeší, **kam** patří pravidlo (jedno
  místo, `AGENTS.md`, ne 18 kopií). Tohle řeší **v jakém jazyce** to místo
  mluví k uživateli za běhu — dvě odlišné osy téhož principu „psát jednou,
  aplikovat opakovaně". Zapsáno jednou v `AGENTS.md` (sekce „Jazyk
  dovednosti"), ne opakováno v každém `SKILL.md`.

---

## 5 · Vědomá omezení, která si PACT-2.0 nechává

Ne každý rozdíl je vylepšení; některé jsou přiznané meze. Tabulka odlišuje
tradeoff (vědomě přijatý) od dosud neověřeného.

| Omezení | Typ | Proč |
|---|---|---|
| Kódové repo `dual-root` není soběstačné | tradeoff | dovednosti a kontext jen z PACT (P6); mitigace P5 |
| Uživatelská úroveň (`$HOME`) se z PACTu nespravuje | vědomě přijato | instalace napáchala víc škody než užitku (`fix-brief-03.md`) |
| RPI v praxi neověřené | dosud neověřeno | adaptace cizí metodiky bez reálného provozu; první kandidát na revizi |
| Zákaz psát kód v Research/Plan stojí na instrukci | slabší záruka | neutrální dovednost nemá `tools:` frontmatter jednoho nástroje |
| Registrace generovaných adaptérů neověřená ve všech runtimech | dosud neověřeno | kanonický `SKILL.md` lze vždy přečíst přímo |
| Runtime arbitráž dovednost vs. plugin není řiditelná | tradeoff | řeší se `AGENTS.md` + `plugin-collision-review`, ne za běhu |
| Tier modelu ovlivňuje **zážitek**, ne **funkčnost** | vlastnost, ne vada | funkčnost (vrstva 1) je nezávislá na tieru; kvalita dialogu (vrstva 2) roste s tierem (UAT běh 5) |

---

## Zdroje

- [nowork-ai/pact-starter](https://github.com/nowork-ai/pact-starter) — původní framework
- [microsoft/hve-core](https://github.com/microsoft/hve-core) — zdroj metodiky RPI a inspirace pro dual root
- [Agent Skills — agentskills.io](https://agentskills.io/home) — standard `SKILL.md`
- [AGENTS.md spec](https://www.morphllm.com/agents-md-guide)
- `docs/ARCHITECTURE.md` — plný destilát rozhodovacího dokumentu
- `docs/DUAL-ROOT.md` · `docs/ROZSAH-KONTEXTU.md` · `docs/VRSTVY.md`
