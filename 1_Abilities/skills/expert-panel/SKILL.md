---
name: expert-panel
description: >-
  Postaví diskuzi několika skutečných odborníků nad tvým rozhodnutím — ne shodu,
  ale produktivní spor, ze kterého vypadne to, co bys sám nenapadlo.
  Use when: uživatel řekne "expert panel", "co by na to řekli odborníci", "svolej panel",
  "potřebuju víc pohledů", "poraď se za mě s experty", "sehraj mi diskuzi",
  "convene an expert panel", "what would experts say". Použij i tehdy, když uživatel
  váhá mezi dvěma variantami zásadního rozhodnutí a chce si je nechat rozebrat.
---

# Expert panel

Model není bytost s názorem, je to simulátor. Když ho necháš „poradit", dostaneš průměr internetu. Když ho necháš zahrát konkrétní lidi, kteří o věci skutečně přemýšleli a **neshodují se**, dostaneš něco použitelnějšího.

Hodnota panelu je ve sporu. Panel, kde všichni souhlasí, je zbytečný.

## Postup

### 1. Rozeber zadání

- Jaké obory se toho týkají?
- Je to rozhodnutí strategické, technické, tvůrčí, nebo hodnotové?
- **Kde by se chytří lidé neshodli?** Tohle je nejdůležitější otázka — určuje složení panelu.
- Chce uživatel nápady, rozhodnutí, plán, nebo prozkoumat terén?

Když je téma příliš široké, polož **jednu** upřesňující otázku. Ne víc.

### 2. Sestav panel

Tři až pět **skutečných** lidí — žijících nebo historických.

| Kritérium | Proč |
|---|---|
| Doložená odbornost | opravdu o tom psali nebo mluvili |
| Odlišné úhly | ne pět variant téhož názoru |
| Produktivní napětí | jejich pohledy si navzájem odporují |
| Různé role | vizionář, praktik, kritik, teoretik |

Pravidla: nejvýš dva lidé z jednoho oboru · vždy aspoň jeden, kdo bude oponovat · vždy aspoň jeden praktik, ne samí teoretici · **nikdy si nevymýšlej experty ani jejich tituly**.

Panel nejdřív navrhni a zeptej se, jestli ho svolat, nebo někoho vyměnit.

### 3. Odehraj diskuzi

Každý mluví svým hlasem — svou terminologií, svými rámci, se svými typickými příklady. Kola:

1. **Úvodní pozice** — každý řekne, jak to vidí
2. **Střet** — vzájemně zpochybňují předpoklady
3. **Průnik** — kde se nečekaně shodnou
4. **Průlom** — myšlenka, která vznikla až srážkou pohledů

### 4. Shrň

Klíčové poznatky, v čem panuje shoda a v čem ne, doporučení ve dvou až třech variantách s různým poměrem rizika a přínosu, další kroky.

## Kam se výstup ukládá

**Panel se vždy ukládá.** Neuložená diskuze je zahozená práce a je to nejčastější způsob, jak o hodnotu téhle dovednosti přijít.

| Situace | Kam |
|---|---|
| panel se týká konkrétního projektu | `0_Projects/<projekt>/expert-panel-RRRR-MM-DD-<téma>.md` |
| panel je obecný a použiješ ho znovu | zeptej se — nabídni `2_Context/expertise/` |
| projekt ještě neexistuje | navrhni založení; po potvrzení spusť `pact new <projekt>` jako agent a teprve pak ulož |

Než zapíšeš, ověř, že soubor téhož jména neexistuje; kdyby ano, přidej `-v2`.

Po uložení napiš uživateli jednou větou, kam to šlo.

**U vícekolových panelů** ukládej průběžně na konci každého kola. Když se diskuze přeruší, ulož, co máš, s poznámkou, že není dokončená.

## Kontext z PACT

- `2_Context/goals/goals.md` — kam uživatel míří. Panel, který doporučí něco proti tomu, má na to upozornit.
- `2_Context/expertise/` — v čem se uživatel vyzná. Nevysvětluj mu základy jeho vlastního oboru.

Když na ně nedosáhneš, panel odehraj i tak a řekni, že jsi kontext neměl.

## Formát výstupu

```markdown
# [Téma] — expert panel

**Datum:** RRRR-MM-DD

## Zadání
[Přeformulovaná otázka, o které se rozhoduje.]

## Panel
### [Jméno]
**Obor:** …
**Úhel pohledu:** [dvě věty]
**Známý čím:** [dílo, pozice, myšlenka]

## Diskuze

### Kolo 1 — úvodní pozice
**[Jméno]:**
> [pozice jeho vlastním hlasem]

### Kolo 2 — střet
**[Jméno] → [Jméno]:**
> [námitka]

**[Jméno] odpovídá:**
> [reakce]

### Průlom
[Myšlenka, která vznikla srážkou. Uveď, čí pohledy se musely potkat.]

## Poznatky
1. **[Název]** — [rozvedení]

## V čem se panel neshodl
| Otázka | Pozice A | Pozice B |

## Doporučení
### Varianta A — [opatrnější]
- **Co:** …
- **Proč:** [z čeho v diskuzi to plyne]
- **Riziko:** …
- **Kdy zvolit:** …

### Varianta B — [odvážnější]
…

## Další kroky
1. …
```

## Kontrola před uložením

1. Poznal by každý z účastníků svůj vlastní hlas?
2. Vypadl z diskuze aspoň jeden poznatek, který není samozřejmý?
3. Dá se na doporučení skutečně jednat?
4. Je ve sporu napětí, které problém osvětluje — nebo si jen zdvořile odporují?

Když je odpověď na druhou otázku ne, panel neodevzdávej. Přehoď složení a zkus to znovu.

## Čeho se vyvarovat

| Ne | Ano |
|---|---|
| vymyšlení odborníci nebo tituly | jen doložitelní lidé |
| slova, která by daný člověk neřekl | držet se jeho známých pozic |
| panel, kde všichni souhlasí | spor je smysl celé věci |
| slavná jména kvůli slávě | vybírat podle relevance |
| doporučení „záleží na okolnostech" | varianty s jasným kdy-co |

## Příklad složení

**Otázka:** „Máme AI stavět vlastní, nebo koupit hotové?"

**Panel:** praktik ze startupového prostředí (zná cenu vlastní stavby) · odborník na nasazování AI (zná technickou realitu) · investor s odporem k utopeným nákladům (bude oponovat) · manažer z velké firmy (zná, co znamená provoz na pět let).

Čtyři lidé, čtyři důvody, proč si navzájem nedají pokoj.
