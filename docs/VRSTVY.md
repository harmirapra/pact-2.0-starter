# Vrstvy schopností

Co všechno agent umí, nepřichází z jednoho místa. PACT staví a spravuje jen první vrstvu; zbylé dvě existují a je dobré vědět, že existují — ale tenhle repozitář je neinstaluje a nemůže.

| Vrstva | Co to je | Přenositelnost | Kde žije |
|---|---|---|---|
| **1. PACT** | tvůj kontext + tvoje dovednosti | plná (otevřený standard) | tenhle repozitář a `$HOME` |
| **2. Rozšíření agenta** | pluginy, marketplace rozšíření, hooks, slash commands | žádná — vendor-specific | konfigurace konkrétního agenta |
| **3. Externí nástroje** | MCP servery, API, SaaS integrace | částečná (MCP je otevřený standard) | mimo rozsah PACT-2.0 v1 |

**Rozhodovací pravidlo:** pokud daná schopnost existuje jako dovednost, dej ji do `1_Abilities/skills/` a máš ji ve všech agentech, které umí `SKILL.md` číst. Rozšíření agenta (vrstva 2) použij jen tam, kde skutečně potřebuješ něco, co dovednost neumí — hooks reagující na událost, slash příkaz, chování při startu session.

## Kolize mezi vrstvou 1 a vrstvou 2

Rozšíření agenta občas pokrývá stejné území jako baseline dovednost z `1_Abilities/skills/` — typicky brainstorming, plánování nebo revize kódu. Tři věci, které je potřeba přiznat na rovinu:

**Runtime arbitráž mezi dovednostmi a rozšířeními není řiditelná.** `SKILL.md` nemá pole pro prioritu ani přednost. Které z nich se při daném dotazu aktivuje první, řídí konkrétní agent, ne PACT — a to se nedá ovlivnit z kanonického zdroje.

**Existují dvě páky, které fungují — a obě mimo runtime:**

| Páka | Kdy působí | Spolehlivost |
|---|---|---|
| `AGENTS.md` | při každém načtení kontextu | vysoká — pravidla se *načítají*, ne vybírají |
| dovednost `scope-review` | periodicky, při správě | vysoká — je to rozhodnutí, ne náhoda |
| popis dovednosti (`description`) | při aktivaci | neřiditelné |

Pravidlo do `AGENTS.md` se uplatní bez ohledu na to, který mechanismus nakonec vystřelí — proto tam patří kontext, ne do jednotlivé dovednosti:

```markdown
Při brainstormingu, plánování nebo strategickém rozhodování si nejdřív
načti 2_Context/expertise/ a 2_Context/goals/goals.md — bez ohledu na to,
který mechanismus se použije.
```

Kolize samotná se řeší při revizi (`scope-review`), ne za běhu — viz jeho `SKILL.md` a `2_Context/stack.md`, kam se rozhodnutí zapisují.

**Baseline dovednost, která ti v prostředí s nainstalovaným rozšířením nikdy nevystřelí, není chyba — je to pojistka** pro prostředí, kde to rozšíření k dispozici nebude (jiný stroj, jiný agent, firemní prostředí bez pluginů). Duplicitní mechanismus je přijatelný; závislost kontextu na tom, který z nich vyhraje, ne.

## Co PACT-2.0 v této vrstvě nedělá

- Neinstaluje ani nespravuje pluginy, marketplace rozšíření ani hooks — ty se instalují v konfiguraci konkrétního agenta, mimo tenhle repozitář.
- Dovednost `pact-setup` (krok 6) rozšíření **jen zaznamená** do `2_Context/stack.md`, neinstaluje je.
- Vrstva 3 (MCP servery, externí API) je vědomě mimo rozsah v1 — kandidát na pozdější fázi, ne teď.
