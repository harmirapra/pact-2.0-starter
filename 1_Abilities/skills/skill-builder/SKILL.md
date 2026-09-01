---
name: skill-builder
description: >-
  Postaví novou dovednost do 1_Abilities/skills/ — složku se SKILL.md, správným
  frontmatterem a popisem, podle kterého se dovednost skutečně aktivuje.
  Use when: uživatel řekne "vytvoř dovednost", "nový skill", "udělej z toho dovednost",
  "postav skill", "napiš SKILL.md", "tohle dělám potřetí, zaslouží si to skill",
  "create a skill", "turn this into a skill", "write a SKILL.md". Použij i tehdy,
  když existující dovednost nefunguje, protože se nespouští.
---

# Skill builder

Dovednost, která se nespustí, neexistuje. Osmdesát procent práce na nové dovednosti je pole `description` — je to jediné, co agent vidí, než se rozhodne dovednost načíst.

## Kdy dovednost vůbec zakládat

Pravidlo eskalace z `AGENTS.md`:

| Stupeň | Kdy | Co udělat |
|---|---|---|
| 0 | jednorázová věc | nic nezakládej, prostě si to řekni |
| 1 | děláš to potřetí | jeden `SKILL.md` |
| 2 | `SKILL.md` přeroste ~500 řádků, nebo se část hodí jen občas | podsložky `references/`, `templates/`, `scripts/` |

**Než začneš stavět, projdi existující dovednosti** v `1_Abilities/skills/`. Když už něco pokrývá stejné území, je skoro vždy lepší rozšířit to existující. Dvě dovednosti na jedno téma spolu v runtime soutěží a kdo vyhraje, neřídíš.

## Než začneš psát

| Otázka | Proč na ní záleží |
|---|---|
| Co má dovednost umožnit? | rozsah |
| **Jakými slovy si o to uživatel řekne?** | tohle je `description` — nejdůležitější odpověď |
| Jak má vypadat výstup? | šablona |
| Kdy se naopak spustit nemá? | negativní hranice v popisu |
| Jaké jsou hraniční případy? | pojistky |

Když uživatel odpovědi už dal v zadání, neptej se znovu.

## Struktura

```
nazev-dovednosti/
├── SKILL.md          ← povinné
├── references/       ← volitelné: podrobnosti, které se nepotřebují vždycky
├── templates/        ← volitelné: šablony výstupů
└── scripts/          ← volitelné: spustitelný kód
```

Název složky **musí** být shodný s polem `name` ve frontmatteru — jinak `pact sync` skončí chybou.

Kebab-case, malá písmena, bez diakritiky.

## Frontmatter

```yaml
---
name: nazev-dovednosti
description: >-
  Co dovednost dělá.
  Use when: [spouštěcí fráze česky], [spouštěcí fráze anglicky].
  Nepoužívej pro [co spadá jinam].
---
```

Povinná jsou obě pole. Nic jiného do frontmatteru nepatří — **zejména ne stav zralosti nebo verze**. Metadata o distribuci patří distributorovi, ne dovednosti.

## Jak psát `description`

Tohle je jádro celé dovednosti. Čti pozorně.

### Pravidla

1. **Buď štědrý na spouštěče.** Vypiš každou frázi a situaci, která má dovednost aktivovat. Agenti spíš nespustí, než aby spustili zbytečně.
2. **Česky i anglicky.** Uživatel střídá jazyky uprostřed práce a dovednost musí chytit obojí. Tohle platí pro spouštěcí fráze v `description` — netýká se to těla dovednosti. Tělo piš česky jako jediný zdroj (žádná duplicitní CZ/EN verze); jakmile se dovednost aktivuje, agent ji vede v jazyce, kterým mluví uživatel, viz `AGENTS.md` sekce "Jazyk dovednosti".
3. **Piš fráze, které uživatel skutečně říká.** Ne oficiální název funkce. Když si o věc říká „projeď mi to", patří do popisu „projeď mi to".
4. **Uveď, kdy dovednost nepoužít.** Zabrání to falešným spuštěním na sousedním území.
5. **Padesát až sto padesát slov.** Míň nestačí na spouštěče, víc zbytečně zabírá kontext.

### Dobrý a špatný popis

❌ `description: Vytváří dovednosti.`

To agentovi neříká nic. Nespustí se.

✅
```yaml
description: >-
  Postaví novou dovednost do 1_Abilities/skills/ — složku se SKILL.md,
  frontmatterem a popisem, podle kterého se dovednost skutečně aktivuje.
  Use when: uživatel řekne "vytvoř dovednost", "nový skill", "postav skill",
  "napiš SKILL.md", "create a skill", "turn this into a skill".
  Nepoužívej na tvorbu promptu — na to je prompt-architect.
```

## Tělo dovednosti

Rozkazovací způsob, ne popis. „Načti", „Ověř", „Zeptej se" — ne „dovednost načítá".

Povinné prvky:

- **aspoň jeden příklad vstup → výstup**; jeden konkrétní příklad učí víc než pět odstavců pravidel
- **odkaz na `2_Context/`** místo natvrdo psaných pravidel — kritéria kvality, styl a doménová znalost patří tam, ne do dovednosti
- **co dělat, když na něco nedosáhne** — na soubor, na cestu, na vyplněný kontext. Dovednost, která v takové chvíli mlčí, vede k tomu, že si agent obsah domyslí.
- **žádné natvrdo psané absolutní cesty** — dovednost musí fungovat i na jiném stroji

Vysvětluj **proč**, ne jen co. Rigidní seznam zákazů agent obchází; důvod respektuje.

Pod 500 řádků. Co je delší nebo se hodí jen občas, jde do `references/`.

## Co do dovednosti nepatří

- vázanost na jeden konkrétní nástroj (názvy slash příkazů, pluginů, konkrétního agenta) — dovednost má fungovat všude
- osobní obsah — jména projektů, klíče, cesty ke konkrétním souborům na tvém stroji
- obecné fráze typu „buď užitečný a důkladný"

## Po dokončení

1. Spusť `3_Tools/bin/pact sync` — vygeneruje adaptéry pro nainstalované agenty
2. Spusť `3_Tools/bin/pact registry` — přepíše `1_Abilities/REGISTRY.md`
3. Navrhni uživateli dvě až tři reálné věty, kterými si o dovednost může říct, ať ověří, že se spouští

Krok 3 nevynechávej. Dovednost, kterou nikdo neotestoval na skutečné formulaci, se typicky nespustí právě tehdy, kdy je potřeba.

## Kontrolní seznam

- [ ] frontmatter má `name` i `description`
- [ ] `name` je shodné s názvem složky, kebab-case
- [ ] `description` obsahuje „Use when" a fráze česky i anglicky
- [ ] `description` říká, kdy dovednost nepoužít
- [ ] tělo je v rozkazovacím způsobu
- [ ] aspoň jeden příklad vstup → výstup
- [ ] odkazuje na `2_Context/` místo vlastních definic
- [ ] říká, co dělat, když na něco nedosáhne
- [ ] žádné absolutní cesty, nic vázaného na jeden nástroj
- [ ] pod 500 řádků
- [ ] `pact sync` a `pact registry` proběhly

## Typické chyby

| Chyba | Proč selže | Místo toho |
|---|---|---|
| vágní popis | dovednost se nespustí | vypiš konkrétní spouštěcí fráze |
| samá MUSÍŠ a NIKDY | agent rigidní pravidla obchází | vysvětli důvod omezení |
| 500+ řádků bez `references/` | zabírá kontext, zpomaluje | podrobnosti do podsložky |
| absolutní cesty | rozbije se na jiném stroji | relativní cesty od kořene PACT |
| žádný příklad | agent si formát výstupu domyslí | jeden pár vstup → výstup |
| dvě dovednosti na totéž | soutěží spolu, arbitráž neřídíš | rozšiř tu existující |
