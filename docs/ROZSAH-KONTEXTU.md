# Rozsah kontextu — tři úrovně, prakticky

## Klíčové zjištění

Instrukční soubory **kaskádují**, dovednosti **ne**.

| | Chování |
|---|---|
| `AGENTS.md` v Copilotu | načte všechny od kořene repa po aktuální složku, spojí; nejbližší má přednost |
| `CLAUDE.md` v Claude Code | prochází strom nahoru až ke `/` a načte každý nalezený |
| Codex | spojí root → cwd, cwd vyhrává konflikty |
| **Dovednosti (`SKILL.md`)** | **neprocházejí rodičovské složky** — hledají se jen v definovaných adresářích |

**Důsledek:** otevřeš-li agenta v podsložce místo v kořeni PACT, instrukční soubory se stejně najdou (kaskádují), ale dovednosti zmizí beze stopy. Nedostaneš chybu — dostaneš jen horší výstup, protože agent dovednost, kterou by jinak použil, prostě nevidí. Neřeší se disciplínou („nezapomeň otevřít kořen"), řeší se tím, že část kontextu je dostupná odjinud než z PACT rootu.

## Tři úrovně

| Úroveň | Co tam patří | Kde reálně leží |
|---|---|---|
| **Uživatelská** (globální) | identita, tone of voice, univerzální dovednosti | `~/.agents/skills`, `~/.copilot/skills`, `~/.copilot/instructions`, `~/.claude/rules`, `~/.claude/CLAUDE.md` |
| **Repo / workspace** | pravidla projektu, projektové dovednosti | `AGENTS.md`, `.github/skills`, `.agents/skills`, `.claude/skills` |
| **Podsložka** | lokální upřesnění | vnořený `AGENTS.md` |

Uživatelská úroveň je dostupná **vždy**, bez ohledu na to, který root máš otevřený — i v cizím kódovém repu, i v podsložce bez vlastního `AGENTS.md`. Proto tam patří jen to, co má agent vidět úplně všude.

## PACT vědomě spravuje jen dvě z těch tří úrovní

**Uživatelská úroveň existuje a chová se přesně takhle bez ohledu na PACT** — je to vlastnost nástrojů (Claude Code, Copilot, …), ne něco, co PACT vymyslel. Do verze `fix-brief-03.md` z ní PACT ale i **zapisoval**: `pact sync` instaloval `2_Context/identity/` do `~/.claude/rules/`, `~/.copilot/instructions/` podle manifestu `2_Context/scope.yml`.

**Tahle instalace skončila.** Ne proto, že by uživatelská úroveň přestala existovat — pořád existuje a pořád kaskáduje — ale protože zápis do ní mimo repo způsobil víc škody než užitku: vymyšlený obsah zapsaný do skutečného `$HOME` bez potvrzení (N-3), manifest, který se neshodoval se smazanými soubory (N-8), neúplný seznam kontrolovaných cest (N-9), a nakonec pojistku, kterou si agent sám obešel přes `--yes` (N-12). Podrobnosti a rozhodnutí: `uat-nalezy.md`, `fix-brief-03.md`.

`pact sync` nezapisuje do konfiguračních cest agentů v `$HOME`
(`~/.claude`, `~/.copilot`, `~/.agents`). Import identity v `pact-setup`,
kroku 1, vede pouze **dovnitř** PACTu. Směr **ven** (instalace) nenahrazuje
nic — kdo chce mít kontext k dispozici i mimo PACT, zkopíruje si ho ručně.

Výchozí stav čerstvé šablony proto vypadá takto:

| | Stav |
|---|---|
| `2_Context/identity/` — about-me, tone of voice | zůstává v PACT; ruční kopie do `$HOME` je na uživateli |
| dovednosti | zůstávají v PACT — generují se jen do `.agents/`, `.claude/`, `.github/` uvnitř repa |
| cíle, expertiza, projekty, projektové dovednosti | zůstávají jen v PACT |
| kanonický originál všeho výše | vždy v PACT |

## Co to stojí — riziko R3, vědomě přijaté

**R3: tichá ztráta kontextu při práci v nižším rootu.** Otevřeš-li agenta v podsložce nebo v jiném repu než PACT, uživatelská úroveň se sice pořád načte (kaskáduje), ale bez ruční kopie v ní nic z PACTu není — a dovednosti (`SKILL.md`) se nenačtou vůbec, protože nekaskádují. Nedostaneš chybu, jen horší výstup.

Práce 2 (instalace do `$HOME`) byla navržené ošetření tohohle rizika. Jejím zrušením riziko **nemizí** — jen se vědomě přijímá, protože náklad na ošetření (kontaminace skutečného `$HOME`, viz N-3/N-8/N-9/N-12) byl vyšší než náklad rizika samotného. Náhradní ošetření:

- **P5 — vstupní bod je vždy PACT.** Nikdy neotvírej kódové repo jako výchozí pracoviště; PACT root je tam, kde dovednosti fungují jistě.
- **Ruční zkopírování**, když se v konkrétním případě ukáže, že kontext v jiném rootu chybí — je to na uživateli, ne na automatice.

## Dvě upozornění

- **Uživatelská úroveň není verzovaná.** Soubory v `$HOME` jsou lokální na stroj a PACT je nespravuje. Kanonický originál zůstává vždy v PACT.
- **Uživatelská úroveň se načítá úplně všude**, včetně firemních repozitářů. Tone of voice tam typicky patří, osobní cíle pravděpodobně ne. Kontrolní otázka u každé ruční kopie: *chci, aby tohle viděl agent při práci nad cizím kódem?*
