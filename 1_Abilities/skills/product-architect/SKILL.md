---
name: product-architect
description: >-
  Převede hrubý nápad na produkt nebo funkci na PRD — zadání, ze kterého se dá stavět
  bez doptávání. Součástí je i implementační brief pro toho, kdo bude psát kód.
  Use when: uživatel řekne "mám nápad na", "chci postavit", "napiš PRD", "specifikace",
  "zadání pro vývoj", "co všechno to má umět", "product spec", "write a PRD",
  "turn this idea into a spec". Použij i tehdy, když uživatel začne popisovat nápad
  a rovnou chce kód — nabídni PRD dřív.
---

# Product architect

Většina špatně postavených věcí byla špatně zadaná. Tahle dovednost převádí nápad na specifikaci, ze které je zřejmé, co se staví, pro koho, a hlavně **co se nestaví**.

## Než začneš

Z popisu nápadu vytěž:

- jaký problém to řeší a komu
- kdo je uživatel
- co to musí umět, aby to k něčemu bylo
- technická omezení, pokud nějaká zazněla
- rozsah — první verze, nebo hotový produkt?

**Chybí-li něco zásadního, zeptej se — maximálně na pět věcí a jen na to, co si nemůžeš rozumně odvodit.** Nikdy nevydávej neúplné PRD. Buď se doptej, nebo dodej celý dokument.

## Kontext z PACT

- `2_Context/expertise/` — doména, ve které uživatel pracuje. Ovlivňuje terminologii i to, co je v jeho oboru samozřejmé.
- `2_Context/goals/goals.md` — čemu má projekt sloužit v širším plánu. Někdy z toho vyplyne, že se má stavět něco jiného.
- `0_Projects/<projekt>/PROJECT.md`, pokud projekt už existuje — typ projektu a kde žije kód.

**Když na tyhle soubory nedosáhneš nebo obsahují `[DOPLNIT]`:** řekni to a pokračuj. PRD bude obecnější; není to důvod nedodat ho.

## Kam výstup patří

Do `0_Projects/<projekt>/PRD.md`. Když projekt ještě neexistuje, navrhni jeho
založení a zeptej se na typ (`single-root` / `dual-root`). Po potvrzení spusť
`pact new <projekt>` jako agent — teprve pak dokument ulož.

**Nikdy neukládej PRD do kódového repozitáře.** Znalostní část projektu žije v PACT (viz `docs/DUAL-ROOT.md`).

## Struktura PRD

```markdown
# [Název]

## 1. Přehled
Odstavec: co to je, pro koho, v čem je hodnota.

## 2. Problém
- Jaký konkrétní problém to řeší?
- Kdo ho má?
- Jak se to řeší dnes a proč to nestačí?

## 3. Uživatel
Hlavní persona: role, bolesti, co pro ni znamená úspěch.

## 4. Funkce první verze
Seřazené podle priority. U každé:
- **Co:** jedna věta
- **Proč:** jaký problém uživatele to řeší
- **Akceptační kritéria:** ověřitelné body
- **Priorita:** musí být / mělo by být / bylo by hezké

## 5. Průchody
Dva až tři nejdůležitější scénáře krok za krokem.

## 6. Struktura
Obrazovky nebo části, navigace, jak spolu data souvisí.

## 7. Principy návrhu
Tři až pět vět, podle kterých se rozhoduje ve sporných místech.
Například: „Rychlost před počtem funkcí."

## 8. Technická stránka
Návrh stacku, integrace, výkonnostní a bezpečnostní požadavky.

## 9. Jak poznáme úspěch
Dvě až čtyři měřitelné veličiny.

## 10. Co se vědomě nedělá
Explicitní výčet. Nejdůležitější sekce celého dokumentu.

## 11. Otevřené otázky
Co je potřeba rozhodnout, než se začne stavět.
```

## Implementační brief

Za PRD připoj samostatnou část pro toho, kdo bude psát kód — ať je to člověk nebo agent.

```markdown
# Implementační brief

## Shrnutí
Dvě až tři věty: co postavit, jaké jsou tvrdé technické požadavky.

## Stack
Frontend / backend / databáze / hosting — každé s jednou větou proč.

## Pořadí stavby
Očíslovaný seznam se závislostmi: co musí být hotové dřív a proč.

## Rozpad na části
Pro každou: účel, vstupy, výstupy, chování, hraniční stavy.

## Datový model
Entity a jejich pole.

## Hraniční případy
| Situace | Očekávané chování |

## Definice hotového
Odškrtávací seznam. Co musí platit, aby se to považovalo za dokončené.
```

## Pravidla pro psaní

1. **Konkrétně, ne vágně.** „Tlačítko má být výrazné" → „Hlavní tlačítko, na mobilu přes celou šířku, výška 48 px, akcentní barva."
2. **Akceptační kritéria musí být ověřitelná.** Špatně: „má to být rychlé." Dobře: „stránka se načte do dvou sekund na pomalém připojení."
3. **Prioritizuj nemilosrdně.** První verze znamená říct ne osmdesáti procentům nápadů.
4. **Předjímej dotazy.** Co by mohlo být dvojznačné, vyjasni dřív, než se někdo zeptá.
5. **Nespecifikuj nemožné.** Nedávej do první verze věci, které by znamenaly měsíce vlastního vývoje.
6. **Odkazuj na známé vzory.** „Jako vyhledávání v Notionu" řekne víc než odstavec popisu.

## Příklad doptání

**Uživatel:** „Chci nástroj, kam vložím odkaz na video a vypadne mi shrnutí."

**Odpověď:**

> Než napíšu PRD, tři věci:
> 1. Webová aplikace, rozšíření prohlížeče, nebo skript na tvém stroji?
> 2. Má si uživatel shrnutí ukládat, nebo je to jednorázová věc?
> 3. Odrážky, souvislý text, nebo časové značky?

Po odpovědích dodej celé PRD i brief. Ne dřív.

## Po dokončení

Když PRD vzniklo pro existující projekt, aktualizuj podle konvence i `0_Projects/<projekt>/architecture.md` — rozhodnutí a jejich zdůvodnění patří tam, ne do PRD.
