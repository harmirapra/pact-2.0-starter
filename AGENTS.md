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

Kanonický zdroj: `1_Abilities/skills/`. Každá dovednost = složka se
`SKILL.md` (YAML frontmatter s `name` + `description`, povinné).

Dovednost se aktivuje podle pole `description` v jejím frontmatteru —
vyber ji podle popisu, nečekej na to, až ji někdo vyjmenuje. Přehled všech
dovedností je v `1_Abilities/REGISTRY.md` (generovaný, needituj ho ručně).

Adresáře `.agents/`, `.claude/` a `.github/` jsou **generované adaptéry** —
vytváří je `3_Tools/bin/pact sync` z kanonického zdroje a jsou v
`.gitignore`. Nikdy do nich needituj ručně a nikdy je necommituj. Změny dělej
v `1_Abilities/skills/` a v `AGENTS.md`, pak spusť `pact sync` a
`pact registry`.

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

## Tvrdá pravidla

1. Při psaní jakéhokoli textu za uživatele načti `2_Context/identity/tone-of-voice/`.
2. Výstupy ukládej do příslušného projektu v `0_Projects/`.
3. NIKDY nekopíruj obsah `2_Context/` do kódových repozitářů.
4. NIKDY nezapisuj tajemství do souborů — patří do `.env` (gitignorováno).
5. U projektu typu `dual-root` si přečti jeho `PROJECT.md` dřív, než sáhneš na kód.
6. Po změně dovednosti spusť `pact sync` a `pact registry`.

## Nastavení / první spuštění

Řekni: "použij dovednost pact-setup".
