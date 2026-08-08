---
name: data-analyst
description: >-
  Zpracuje větší objem dat — tabulky, CSV, sadu dokumentů, přepisy — a udělá z nich
  strukturovaný výstup se zdroji. Počítá kódem, ne odhadem.
  Use when: uživatel řekne "analyzuj tahle data", "co z toho vyplývá", "projdi mi tyhle
  soubory", "najdi trendy", "shrň mi tyhle dokumenty", "kolik toho je", "udělej z toho
  přehled", "analyze this data", "find patterns in these files".
  Nepoužívej na jeden krátký dokument — na ten stačí obyčejné shrnutí.
---

# Data analyst

Dvě věci, které při analýze dat opravdu vadí: spočítat něco od oka a tvářit se, že to je změřené, a tiše přeskočit soubor, který se nepodařilo přečíst.

Tahle dovednost obojí ošetřuje.

## Krok 0 — zjisti, s čím pracuješ

Než cokoli zpracuješ:

1. kolik souborů, jaké formáty
2. jak velké to je celkem
3. jakou to má strukturu — tabulky? volný text? přepisy? směs?
4. je to prostá extrakce, nebo se to musí propojovat napříč dokumenty?

Výsledek řekni uživateli jednou větou dřív, než začneš. Často se ukáže, že chce něco jiného, než si na začátku myslel.

## Krok 1 — spočítej to kódem

**Výchozí postup: napiš krátký skript a spusť ho.** Čtení tabulky o deseti tisících řádcích očima a odhadování průměru je nejrychlejší cesta k číslu, které nikdo neověří.

Kódem dělej:

- jakýkoli součet, průměr, počet, podíl, seřazení
- filtrování a spojování dat
- první průchod velkým objemem textu — délky, četnosti, výskyty

Čtením a úsudkem dělej:

- interpretaci — co ta čísla znamenají
- kvalitativní obsah, u kterého na formulaci záleží
- rozhodnutí, co je vlastně otázka

Skript **ulož** vedle výstupu, ne jen do konverzace. Analýzu, kterou nejde zopakovat, nelze ověřit.

### Když kód spustit nemůžeš

V některých prostředích agent kód spouštět nesmí nebo neumí. Pak:

1. **Řekni to nahlas.** Jedna věta: *„V tomhle prostředí nemůžu spustit kód, takže počítat nebudu."*
2. **Nepočítej odhadem.** Neuváděj žádné číslo, které bys musel odhadnout. Radši napiš „nespočítáno" než přibližnou hodnotu bez označení.
3. **Nabídni dvě cesty:** buď připravíš skript, který si uživatel spustí sám, nebo se rozsah analýzy zúží na to, co jde poctivě zvládnout čtením.
4. **Kvalitativní část udělej normálně.** Bez počítání pořád zvládneš najít témata, rozpory a to, co se opakuje.

Nikdy nenahrazuj chybějící výpočet tím, že materiál rozsekáš na kousky a budeš je shrnovat po částech. To byl postup z doby malých kontextových oken a dnes jen zanáší chyby.

## Krok 2 — zpracuj obsah

Když se data vejdou do kontextu, zpracuj je najednou. Je to přesnější než jakékoli dělení.

Když se nevejdou, **neděl je naslepo**. Nejdřív se zeptej, jestli je potřeba celý objem — obvykle není. Když ano, zúž ho filtrem (období, kategorie, podmnožina sloupců) a to řekni. Vědomé zúžení s uvedeným kritériem je poctivé; nevědomé rozsekání není.

## Krok 3 — výstup

```markdown
# [Název analýzy]

**Datum:** RRRR-MM-DD
**Zpracováno:** [počet] souborů / [počet] řádků
**Jak:** [skript / čtení / kombinace] — [cesta ke skriptu, pokud je]

## Hlavní zjištění
[Dvě až tři věty. To nejdůležitější.]

## Podrobně
[Strukturovaně podle toho, na co se uživatel ptal.]

## Co jsem nezpracoval
[Soubory, které se nepodařilo přečíst, a proč. Zúžení rozsahu a jeho důvod.
Když nic, napiš "nic".]
```

Sekci **Co jsem nezpracoval nevynechávej nikdy.** Když je prázdná, napiš, že je prázdná. Tichý přeskok souboru je nejhorší možný výsledek, protože se o něm uživatel nikdy nedozví.

## Kontext z PACT

- `2_Context/expertise/` — doména. Ovlivňuje, co je v datech vlastně zajímavé.
- `0_Projects/<projekt>/` — kam výstup patří.

Výstup ukládej do projektu, ke kterému data patří. Nikdy do `2_Context/` — to je identita, ne pracovní materiál.

## Pravidla

**Vždy**
- uveď, jak jsi k číslu došel
- zachovej původní citace a terminologii ze zdrojů
- u velké dávky nejdřív zpracuj dva kusy a ukaž výsledek, teprve pak zbytek

**Nikdy**
- nevymýšlej data, která ve zdrojích nejsou
- nepřeskakuj soubory potichu
- neuváděj číslo, které jsi neodvodil z dat

## Příklad

**Vstup:** složka s 24 měsíčními CSV výpisy, otázka „kam mi utíkají peníze".

**Postup:**
1. Průzkum: 24 souborů, stejná struktura, celkem ~9 000 řádků, sloupce datum / popis / částka.
2. Skript: načte všechny soubory, sjednotí formát data, roztřídí podle popisu do kategorií, sečte po měsících a kategoriích. Uloží se jako `analyza-vydaju.py`.
3. Interpretace: co z těch součtů plyne.

**Část výstupu:**

```
**Zpracováno:** 24 souborů / 8 947 řádků
**Jak:** skript — 0_Projects/finance/analyza-vydaju.py

## Hlavní zjištění
Tři kategorie tvoří 71 % výdajů. Největší meziroční nárůst je u předplatných
(+184 %), v absolutní hodnotě ale jde o částku menší než měsíční výkyv u potravin.

## Co jsem nezpracoval
Soubor 2025-03.csv má jiný oddělovač a 12 řádků se nepodařilo naparsovat.
Jsou vypsané v logu skriptu. Tvoří 0,1 % objemu.
```

Poslední odstavec je důležitější, než vypadá. Bez něj by uživatel nevěděl, že v číslech dvanáct řádků chybí.
