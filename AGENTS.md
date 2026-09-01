# AGENTS.md

## Co je tento repozitář

**PACT** — osobní AI workspace. Kontext, dovednosti a znalostní část
projektů, organizované tak, aby jakýkoli AI agent (Claude Code, GitHub
Copilot, Cursor, Windsurf, ...) produkoval méně generický, víc
personalizovaný výstup.

Tohle není softwarový projekt v obvyklém smyslu — není tu build ani lint.
Práce v tomhle repu znamená číst a psát markdown, ne psát a spouštět kód,
pokud tě uživatel výslovně nepožádá o práci uvnitř `3_Tools/`.

Kód s vlastním životním cyklem (commity, verze, nasazení) **není** v tomto
repu, pokud pro něj uživatel nezaložil projekt typu `single-root` uvnitř
`3_Tools/` nebo `0_Projects/<projekt>/`. Projekty typu `dual-root` mají kód
v paralelním kořeni vedle PACTu — viz `docs/DUAL-ROOT.md`.

## Architektura: čtyři pilíře

| Složka | Otázka | Obsah |
|---|---|---|
| `0_Projects/` | CO dělám? | Znalostní část projektů a jejich výstupy |
| `1_Abilities/` | JAK to dělat? | Dovednosti — složky se `SKILL.md`, otevřený standard [Agent Skills](https://agentskills.io) |
| `2_Context/` | KDO jsem / co dělám? | Identita, tone of voice, cíle, expertiza |
| `3_Tools/` | S ČÍM? | CLI, skripty, znovupoužitelné nástroje |

**Single Source of Truth:** osobní kontext žije jen v `2_Context/`;
dovednosti na něj odkazují, nekopírují ho. Při psaní obsahu za uživatele
nebo při editaci dovednosti vždy nejdřív načti relevantní soubory z
`2_Context/` (zejména `identity/tone-of-voice/` a `identity/about-me.md`).

## Dovednosti

Kanonický zdroj: `1_Abilities/skills/<název>/SKILL.md`. Každou dovednost
můžeš prostě přečíst a řídit se jí — registrace v runtime není podmínka.
`SKILL.md` má povinný YAML frontmatter s `name` + `description`.

Dovednost se aktivuje podle pole `description` v jejím frontmatteru —
vyber ji podle popisu, nečekej na to, až ji někdo vyjmenuje. Přehled všech
dovedností je v `1_Abilities/REGISTRY.md` (generovaný, needituj ho ručně).

Adresáře `.agents/`, `.claude/` a `.github/` jsou **generované adaptéry** —
vytváří je `3_Tools/bin/pact sync` z kanonického zdroje a jsou v
`.gitignore`. Nikdy do nich needituj ručně a nikdy je necommituj. Změny dělej
v `1_Abilities/skills/` a v `AGENTS.md`, pak spusť `pact sync` a
`pact registry`. Některé runtimy dovednosti z adaptérů zaregistrují samy,
jiné ne; když registrace není dostupná, otevři kanonický `SKILL.md` přímo.

### Jazyk dovednosti

Aktivace (pole `description`) je dvojjazyčná už dnes — spouštěcí fráze
musí chytit češtinu i angličtinu (`skill-builder`, pravidlo #2). To ale
neznamená dvojjazyčné tělo. Tělo `SKILL.md` je psané česky jako jediný
autorský zdroj (žádná duplicitní CZ/EN verze k údržbě), ale **jakmile se
dovednost aktivuje, veď zbytek interakce — otázky, mezikroky, výstup — v
jazyce, kterým mluví uživatel/vstup**, ne nutně v jazyce, ve kterém je
napsané tělo souboru. Stejný princip, jakým se řídí i tahle instance PACT
sama vůči svému vlastnímu obsahu.

## PACT není celý ekosystém

Ne všechno, co agent pro práci potřebuje, je v tomhle repu. Část schopností
může přicházet z rozšíření konkrétního AI nástroje (pluginy, marketplace,
hooks, slash commands) — ta žijí mimo repo, na úrovni runtime daného
nástroje, a liší se agent od agenta. Podrobně viz `docs/VRSTVY.md`.

Pokud narazíš na odkaz na dovednost nebo schopnost, kterou v repu nevidíš a
ani ji nemáš ve svém runtime, nepředpokládej, že neexistuje a nesnaž se ji
nahradit improvizací — řekni to uživateli a zeptej se, čím je to u něj
zajištěné.

## Povinná retrospektiva release (u každého projektu)

Každý projekt pod `0_Projects/` má mít dva žijící dokumenty: `PRD.md`
(co/proč — rozsah, workflow, otevřené otázky) a `architecture.md` (jak —
rozhodnutí a jejich zdůvodnění, známá omezení).

Po dokončení smysluplného kusu práce v projektu (nová funkce, funkční krok)
udělej z vlastní iniciativy, bez čekání na vyzvání:

1. Aktualizuj `PRD.md`, ať odpovídá tomu, co se opravdu postavilo. Vyřešené
   otevřené otázky přesuň do "Vyřešené otázky", nemaž je.
2. Zapiš získanou znalost — rozhodnutí, zdůvodnění, omezení — do
   `architecture.md`.
3. Nahlas uživateli krátké shrnutí toho, co se změnilo.

## RPI — Research → Plan → Implement → Review

Čtyři dovednosti (`rpi-research`, `rpi-plan`, `rpi-implement`, `rpi-review`,
v `1_Abilities/skills/`) nahrazují řetěz promptů v jedné konverzaci
strukturovaným postupem se čtyřmi oddělenými fázemi a artefakty na disku
v `0_Projects/<projekt>/rpi/`.

**Kdy RPI a kdy rovnou rychlá úprava:**

| RPI | Rychlá úprava |
|---|---|
| změna zasahuje víc souborů | překlep |
| učíš se nový vzor nebo API | přidání logu |
| jsou v tom externí závislosti | refaktor pod 50 řádků |
| zadání není jasné | změna je zjevná |

Pravidlo palce: *musíš něčemu rozumět, než to implementuješ? → RPI.*

**Když zadání odpovídá profilu RPI, navrhni RPI a počkej na rozhodnutí —
dřív než začneš psát kód.** Neaplikuj tiše ani jednu variantu sám;
uživatel má vždycky vidět, že se rozhoduje.

Mezi fázemi **vyčisti kontext** (nová konverzace — v nástrojích s příkazem
na vyčištění kontextu, např. `/clear`, ho použij). Je to jediný krok RPI,
který nezajistí ani agent sám, ani tenhle soubor — bez něj RPI degraduje
zpátky na řetěz promptů v jedné konverzaci a většina přínosu zmizí.

## Tvrdá pravidla

1. Při psaní jakéhokoli textu za uživatele načti `2_Context/identity/tone-of-voice/`.
2. Výstupy ukládej do příslušného projektu v `0_Projects/`.
3. NIKDY nekopíruj obsah `2_Context/` do kódových repozitářů.
4. NIKDY nezapisuj tajemství do souborů — patří do `.env` (gitignorováno).
5. U projektu typu `dual-root` si přečti jeho `PROJECT.md` dřív, než sáhneš na kód.
6. Po změně dovednosti spusť `pact sync` a `pact registry`.
7. **Uživatel mluví, agent obsluhuje.** Uživatel popíše potřebu; příkazy `3_Tools/bin/pact` spouští agent.
8. Do konfiguračních cest agentů (`~/.claude`, `~/.copilot`, `~/.agents`) PACT nezapisuje. Je to území nástroje, ne workspace.

## Nastavení / první spuštění

Uživatel řekne: *„pomoz mi nastavit tento pact"*. Funguje to i v runtime,
který dovednost `pact-setup` nezaregistroval — přečti
`1_Abilities/skills/pact-setup/SKILL.md` a řiď se jím.

Kdykoli později může říct: *„pověz mi, jak používat tento pact"*.
