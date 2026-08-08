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

## Výchozí rozdělení

Repo dodává mechanismus, ne názor o tom, co konkrétně je pro tebe globální — to se kurátoruje za provozu (viz dovednost `scope-review`, přibude ve fázi F5). Výchozí stav čerstvé šablony:

| | Výchozí stav při iniciaci |
|---|---|
| `2_Context/identity/` — about-me, tone of voice | **na uživatelskou úroveň** |
| dovednosti | **žádné** — uživatelská úroveň startuje prázdná |
| cíle, expertiza, projekty, projektové dovednosti | zůstávají jen v PACT |
| kanonický originál všeho výše | vždy v PACT |

Posun jakékoli dovednosti nebo dalšího kontextu na uživatelskou úroveň je vědomé rozhodnutí, ne výchozí nastavení.

## `2_Context/scope.yml`

Manifest toho, co `pact sync` instaluje do `$HOME`:

```yaml
user_level:
  context:
    - identity/about-me.md
    - identity/tone-of-voice/
  skills: []   # startuje prázdné
```

`pact sync` bez argumentů přečte `scope.yml` a vedle regenerace adaptérů (`.agents/`, `.claude/`, `.github/`) zkopíruje položky `context` do `~/.copilot/instructions/` a `~/.claude/rules/`, a položky `skills` do `~/.agents/skills/`, `~/.copilot/skills/` a `~/.claude/skills/`. `pact sync --dry-run` totéž jen vypíše, nic nezapisuje.

Před přepsáním souboru v `$HOME`, který nevznikl předchozím `pact sync`, se zeptá — v interaktivním běhu na potvrzení, v neinteraktivním soubor přeskočí a nahlásí to.

## Dvě upozornění

- **Uživatelská úroveň není verzovaná.** Soubory v `$HOME` jsou lokální na stroj. Kanonický originál zůstává v PACT; na novém stroji je `pact sync` součástí bootstrapu (`pact-setup`, krok 4).
- **Uživatelská úroveň se načítá úplně všude**, včetně firemních repozitářů. Tone of voice tam typicky patří, osobní cíle pravděpodobně ne. Kontrolní otázka u každé položky: *chci, aby tohle viděl agent při práci nad cizím kódem?*
