---
name: markdown-to-html
description: >-
  Převede Markdown na samostatný HTML soubor — čitelnou typografií, obsahem, tabulkami
  a barevným vyznačením změn. Bez externích závislostí, výstup je jeden soubor.
  Use when: uživatel řekne "udělej z toho HTML", "převeď na HTML", "chci to poslat
  jako stránku", "vyexportuj to do PDF", "vytiskni to", "hezky to naformátuj",
  "vyznač v tom změny", "convert to HTML", "make this printable".
  Nepoužívej na tvorbu webu — tohle dělá jeden dokument, ne stránky.
---

# Markdown → HTML

Převod dělá **skript**, ne ty. Dva důvody: výsledek je pokaždé stejný a chyby v převodu jsou dohledatelné.

```bash
python3 1_Abilities/skills/markdown-to-html/scripts/md2html.py vstup.md
```

Vznikne `vstup.html` vedle vstupu. Je to jeden soubor — CSS uvnitř, žádné externí závislosti — takže se dá poslat e-mailem, otevřít offline i vytisknout do PDF.

## Přepínače

| Přepínač | K čemu |
|---|---|
| `-o soubor.html` | jiné umístění výstupu |
| `--style modern` | bezpatkové písmo (výchozí) |
| `--style book` | patkové písmo, na dlouhé čtení |
| `--title "Název"` | titulek stránky, jinak se bere první nadpis H1 |

Vstup `-` čte ze standardního vstupu.

## Vyznačení změn

Když má být z dokumentu vidět, co se změnilo, obal části textu značkami. Značka může obalit celý blok (na samostatných řádcích) nebo kus věty.

```markdown
{NEW}Nový text, který v původní verzi nebyl.{/NEW}

{UPDATE}Text upravený oproti původní verzi.{/UPDATE}

{DELETE}Text, který má zmizet.{/DELETE}

{NOTE}Poznámka redaktora.{/NOTE}

{ORIGINAL}Původní znění pro srovnání.{/ORIGINAL}
```

Ve výstupu dostane každá značka svou barvu a nahoře přibude vysvětlivka — ale jen těch značek, které se v dokumentu skutečně vyskytly.

Blokové značky mohou uvnitř obsahovat další Markdown včetně seznamů a tabulek.

## Co skript umí

Nadpisy · odstavce · **tučné**, *kurzívu*, ~~přeškrtnutí~~, `kód` · odkazy · obrázky · seznamy odrážkové, číslované, zanořené i zaškrtávací (`- [x]`) · tabulky včetně zarovnání (`:---:`) · bloky kódu s označením jazyka · citace · vodorovné čáry · obsah, který se vygeneruje sám při třech a více nadpisech.

Výstup je responzivní, umí světlý i tmavý režim podle nastavení systému a má vlastní styl pro tisk.

## Co skript neumí

Odkazy přes referenci (`[text][id]`) · poznámky pod čarou (`[^1]`) · nadpisy podtržené `===` nebo `---` · vnořené citace · definiční seznamy.

**Skript to nezamlčí.** Co nepřevede, vypíše na chybový výstup i s číslem řádku:

```
Nepřevedeno nebo převedeno doslovně:
  řádek 57    odkaz přes referenci    Odkaz přes referenci [takhle][ref]...
  řádek 61    externí obrázek         https://example.com/x.png

Celkem 2 místa. Zkontroluj je ve výstupu.
```

**Tenhle výpis vždy přečti a shrň uživateli.** Když ho spolkneš, uživatel se o vadných místech dozví až od příjemce dokumentu.

Poznámka k obrázkům: skript je převede, ale odkaz na cizí server znamená, že dokument přestane být samostatný — bez internetu se obrázek nezobrazí. Chceš-li ho mít uvnitř, vlož ho jako `data:` URI.

## Když skript nemůžeš spustit

V prostředí bez spouštění kódu HTML **nepiš ručně místo skriptu**. Ručně napsaný výstup vypadá pokaždé jinak a nikdo ho nezkontroluje. Místo toho:

1. řekni, že v tomhle prostředí skript spustit nejde
2. dej uživateli přesný příkaz, který si spustí sám
3. nabídni, že mezitím projdeš dokument a řekneš, co skript nepřevede

## Příklad

**Vstup** `zapis.md`:

```markdown
# Zápis z porady

Domluvili jsme se na odkladu.

{NEW}Nově: termín se posouvá na 15. dubna.{/NEW}

| Úkol | Kdo |
|---|---|
| Ověřit ceny | Jana |
```

**Příkaz:**

```bash
python3 1_Abilities/skills/markdown-to-html/scripts/md2html.py zapis.md --style book
```

**Výstup:** `zapis.html` — titulek „Zápis z porady", odstavec, růžově orámovaný blok s popiskem NOVÝ TEXT, tabulka a nahoře vysvětlivka barev. Bez obsahu, protože dokument má jen jeden nadpis.

## Kam soubor patří

Do složky projektu v `0_Projects/`, ke zdrojovému Markdownu. HTML je odvozený artefakt — když se zdroj změní, převod se pustí znovu. Neupravuj vygenerovaný HTML ručně; příští převod to přepíše.
