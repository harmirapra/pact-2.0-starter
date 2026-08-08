---
name: prompt-architect
description: >-
  Převede vágní požadavek na strukturovaný prompt pro LLM — s personou, kontraktem
  na výstup, příklady a pojistkami proti typickým selháním.
  Use when: uživatel řekne "vytvoř prompt", "napiš prompt", "system prompt",
  "prompt pro AI", "zadání pro agenta", "vylepši tenhle prompt", "proč mi tenhle
  prompt nefunguje", "create a prompt", "write a system prompt", "improve this prompt".
  Nepoužívej pro tvorbu dovednosti — na to je skill-builder.
---

# Prompt architect

Vágní zadání dá vágní výstup. Tahle dovednost převádí „napiš mi něco o X" na prompt, který má definovaný cíl, tvar výstupu a hranice.

## Kdy tuhle dovednost použít a kdy ne

| Použij | Nepoužívej |
|---|---|
| prompt se bude používat opakovaně | jednorázový dotaz — prostě se zeptej |
| prompt předává práci jinému agentovi nebo modelu | chceš dovednost do `1_Abilities/` → `skill-builder` |
| existující prompt dává nekonzistentní výsledky | chceš zpracovat data → `data-analyst` |

## Než začneš psát

Nejdřív si zodpověz čtyři otázky. Když na některou neznáš odpověď a nejde odvodit ze zadání, **zeptej se uživatele** — maximálně na tři věci najednou.

| Otázka | Co z ní plyne |
|---|---|
| Jak vypadá úspěch? | cílový výstup |
| Kdo výstup použije? | tón a míra podrobnosti |
| Co by znamenalo selhání? | pojistky, které je potřeba zakódovat |
| Je to jednorázová, nebo opakovaná úloha? | jestli má smysl investovat do struktury |

**Antipattern:** začít psát prompt dřív, než víš, k čemu má vést.

## Kontext z PACT

Pokud prompt vzniká pro uživatelovu vlastní práci — tedy ne jako obecná ukázka — načti dřív, než začneš:

- `2_Context/identity/about-me.md` — kdo je autor, v jaké roli prompt používá
- `2_Context/identity/tone-of-voice/` — když má výstup promptu znít jako uživatel
- `2_Context/expertise/` — doménová terminologie, kterou má prompt používat

**Když na tyhle soubory nedosáhneš nebo obsahují jen `[DOPLNIT]`:** řekni to nahlas a pokračuj s obecným promptem. Nedomýšlej, kdo uživatel je.

## Stavba promptu

### 1. Konkrétní persona, ne obecná role

❌ „Jsi marketingový expert."
✅ „Jsi B2B SaaS growth marketer s deseti lety praxe. Vyškáloval jsi tři startupy z 1 na 20 milionů ARR. Rozhoduješ se podle dat a jsi skeptický k marnivým metrikám."

Rozdíl není v délce. Je v tom, že druhá verze obsahuje **postoj** — a ten se propíše do každé odpovědi.

### 2. Kontrakt na výstup

Formát, struktura a délka explicitně:

```
VÝSTUP:
- Formát: Markdown s nadpisy úrovně 2
- Délka: 400–600 slov
- Struktura: Problém → Analýza → 3 doporučení → Další krok
- Tón: přímý, bez korporátního žargonu
```

### 3. Doménový kontext

Terminologie, rámce, omezení:

```
KONTEXT:
- Obor: česká výroba, střední firmy (50–200 zaměstnanců)
- Omezení: řešení musí fungovat bez vlastního IT
- Rámec: pravidlo 90/10 — soustřeď se na kroky s největším dopadem
```

### 4. Jeden příklad místo pěti odstavců pravidel

Ukázka vstup → výstup naučí model víc než popis. Jeden dobrý příklad stačí; dva jsou lepší, když se úloha větví.

### 5. Pojistky proti konkrétním selháním

Ne obecné „buď kvalitní", ale konkrétní zákazy:

```
OMEZENÍ:
- Nikdy nepiš „záleží na okolnostech", „zvažte", „možná byste chtěli"
- Vždy uveď konkrétní čísla, termíny nebo metriky
- Když informace chybí, zeptej se — nedomýšlej
- Maximálně jedna otázka na odpověď
```

## Kontrola před odevzdáním

| Test | Otázka |
|---|---|
| Srozumitelnost | Pochopil by přesně, co má dělat, chytrý člověk bez kontextu? |
| Hraniční případ | Jaký nejpodivnější vstup může přijít? Zvládne ho prompt? |
| Selhání | Jak by mohl vzniknout špatný výstup? Je to ošetřené? |
| Úspornost | Dá se některá věta smazat bez ztráty významu? |

## Výstup dovednosti

Odevzdej dvě části:

```
NÁZEV: [výstižný název]
K ČEMU: [jedna věta — jaký problém prompt řeší]
KDY POUŽÍT: [situace]
CO MUSÍ UŽIVATEL DODAT: [vstupy]
```

a pod tím samotný prompt ve struktuře: persona → kontext → úkol → formát výstupu → příklad → omezení → případný ověřovací krok.

## Příklad

**Vstup od uživatele:** „Potřebuju prompt, co mi shrne poznámky z porady."

**Doptání (protože chybí cíl a příjemce):**
1. Pro koho je shrnutí — pro tebe, nebo se rozesílá účastníkům?
2. Co s ním má čtenář udělat — jen si přečíst, nebo z něj plynou úkoly?

*Uživatel: „Rozesílá se účastníkům, hlavní je, aby bylo jasné, kdo co má udělat."*

**Výstup:**

```
NÁZEV: Zápis z porady s úkoly
K ČEMU: Převede syrové poznámky na zápis, ze kterého je zřejmé, kdo co má udělat a dokdy.
KDY POUŽÍT: Po každé poradě, ze které plynou úkoly.
CO MUSÍ UŽIVATEL DODAT: Syrové poznámky nebo přepis, datum porady, seznam účastníků.

---

Jsi zkušený projektový manažer, který za patnáct let odpsal několik tisíc zápisů.
Víš, že zápis, ze kterého není jasné, kdo co má udělat, je ztráta času všech
zúčastněných.

VSTUP: Syrové poznámky z porady, datum, účastníci.

ÚKOL: Vytvoř zápis, který účastníkovi po týdnu připomene, na čem se domluvili.

VÝSTUP:
- Formát: Markdown
- Struktura: Závěry (max 5 odrážek) → tabulka úkolů → otevřené otázky
- Tabulka úkolů má sloupce: Úkol | Kdo | Dokdy
- Délka: maximálně jedna obrazovka

PŘÍKLAD ŘÁDKU ÚKOLU:
| Ověřit cenu licencí u dodavatele | Jana | 15. 3. |

OMEZENÍ:
- Když u úkolu chybí zodpovědná osoba nebo termín, napiš do buňky "NEDOHODNUTO"
  a uveď to v otevřených otázkách. Nikoho nedosazuj.
- Nepřepisuj diskuzi. Zapiš, na čem se skupina shodla.
- Když z poznámek nejde poznat závěr, napiš to místo vymyšlení závěru.
```

## Pokročilé techniky

| Technika | Kdy | Jak |
|---|---|---|
| Uvažování krok za krokem | složité odvozování | „Nejdřív si problém rozeber, teprve pak odpověz" |
| Sebeověření | výstupy s vysokou cenou chyby | „Na konci uveď, čím si nejsi jistý" |
| Strukturovaný výstup | extrakce dat | zadej JSON schéma explicitně |
| Negativní příklad | opakující se konkrétní chyba | ukaž vedle dobrého i špatný výstup |
