---
name: knowledge-extractor
description: >-
  Z hromady zdrojů na jedno téma — článků, studií, přepisů, dokumentace — vytáhne
  ověřitelný znalostní výtah: principy, rozhodovací pravidla, typické chyby a to,
  kde si zdroje odporují. Výtah je pak podkladem pro novou dovednost.
  Use when: uživatel řekne "mám nastudováno X článků", "udělej z toho znalostní bázi",
  "vytáhni z toho podstatné", "nastuduj to a shrň mi pravidla", "chci z toho udělat
  dovednost", "extract knowledge from these sources", "build a knowledge base from this".
  Nepoužívej na jeden dokument — na ten stačí obyčejné shrnutí.
  Nepoužívej na číselná/tabulková data — na to je data-analyst.
---

# Knowledge extractor

Deset článků na jedno téma je pořád jen deset článků. Tahle dovednost z nich udělá něco, podle čeho se dá rozhodovat: pravidla, hranice tématu a poctivě přiznané rozpory mezi zdroji.

## Kdy to má smysl

- máš zhruba 5 až 50 zdrojů na jedno téma
- chceš z nich vyrobit dovednost, kterou budeš používat opakovaně
- potřebuješ znalostní bázi, u které jde dohledat, odkud co je

**Na jeden dokument tohle nepoužívej.** Tam stačí říct „shrň mi to".

## Fáze 1 — zmapuj téma

Než začneš vytahovat detaily, projdi materiál a odpověz si:

| Otázka | Co hledáš |
|---|---|
| Hranice tématu | Co ještě patří dovnitř? Co už ne? Kde je šedá zóna? |
| Shoda a spor | V čem se zdroje shodují? Kde se rozcházejí? |
| Trvanlivost | Co zastará za rok? Co platí pořád? |
| Použitelnost | Co jde použít hned? Co je spíš teorie? |

Hranice zapiš explicitně — je to nejužitečnější věc z celé fáze:

```
Patří:      syntaxe promptu, styly, negativní prompty, poměry stran
Nepatří:    provoz serverů, trénování vlastních modelů
Šedá zóna:  následné úpravy v grafickém editoru
```

## Fáze 2 — vytáhni znalostní bloky

Ke každému bloku **vždy zdroj**. Tvrzení bez dohledatelného původu do výtahu nepatří.

**Pojmy s definicí**

```
POJEM:    Negativní prompt
DEFINICE: Instrukce, co model nemá generovat
PŘÍKLAD:  "no text, no watermark"
ZDROJ:    [název dokumentu nebo odkaz]
```

**Postupy** — pojmenované, s kroky, se zdrojem.

**Rozhodovací pravidla** ve tvaru když–tak. Tohle je nejcennější část výtahu, protože se z ní přímo staví dovednost:

```
KDYŽ  cíl = fotorealistický portrét
TAK   použij: "85mm, malá hloubka ostrosti, studiové světlo"
NE    "malba", "ilustrace"
```

**Typické chyby** — co lidé dělají špatně, proč to nefunguje, co dělat místo toho.

## Fáze 3 — rozsuď rozpory

Zdroje si budou odporovat. Nepřecházej to mlčky.

| Situace | Co s tím |
|---|---|
| A tvrdí X, B tvrdí Y | uveď obojí i s tím, kdy platí které |
| starší proti novějšímu | preferuj novější, ale napiš, co se změnilo |
| obecná rada proti konkrétní | pro konkrétní použití vyhrává konkrétní |
| jeden zdroj proti všem ostatním | zmiň to jako menšinový názor, nezahazuj bez uvedení |

## Fáze 4 — sepiš výtah

**Rozsah: 500 až 800 slov.** Delší výtah se nečte a při použití zabírá kontext, který by měl patřit datům.

```markdown
# Znalostní výtah: [téma]

**Zdrojů:** [počet] · **Datum:** RRRR-MM-DD

## Hranice tématu
Patří / nepatří / šedá zóna.

## Základní principy
Nejvýš pět, každý s jednou větou vysvětlení a zdrojem.

## Klíčová terminologie
| Pojem | Význam | Zdroj |

## Postupy
Jeden až dva hlavní, s kroky.

## Rozhodovací pravidla
Když–tak.

## Typické chyby
Chyba → proč vadí → co místo toho.

## Jak poznat dobrý výsledek
Odškrtávací seznam a varovné signály.

## Kde si zdroje odporují
Otevřeně, ne zahlazeně.

## Použité zdroje
Číslovaný seznam.
```

Výtah ulož do `0_Projects/<projekt>/` nebo — když je to znalost použitelná napříč projekty — do `2_Context/expertise/`. Zeptej se, kam patří, když to není zřejmé.

## Fáze 5 — předání

Výtah **není** dovednost. Když z něj má vzniknout `SKILL.md`, předej ho dovednosti `skill-builder` — ta ví, jak napsat `description`, podle kterého se dovednost skutečně aktivuje.

Řekni to uživateli takhle: *„Výtah je hotový v [cesta]. Mám z něj postavit dovednost? Použil bych na to `skill-builder`."*

Rozdělení práce je záměrné: tahle dovednost ověřuje **znalost**, `skill-builder` řeší **aktivaci a formát**. Kdyby to dělala jedna dovednost, dělala by obojí hůř.

## Kontrola před odevzdáním

| Test | Otázka |
|---|---|
| Dohledatelnost | Dá se každé tvrzení najít ve zdrojích? |
| Konkrétnost | Má každé pravidlo příklad? |
| Použitelnost | Ví čtenář, co má dělat v každé z popsaných situací? |
| Úspornost | Dá se něco smazat bez ztráty hodnoty? |
| Poctivost | Jsou rozpory mezi zdroji přiznané, nebo zamlčené? |

## Když nedosáhneš na zdroje

Uživatel často odkáže na materiál, na který nevidíš — složku mimo dosah, sdílený disk, odkaz za přihlášením. **Neodvozuj obsah z názvu souboru a nedoplňuj ho z obecné znalosti.** Řekni, na co nedosáhneš, a navrhni, jak to zpřístupnit. Výtah postavený zčásti na domněnkách je horší než žádný, protože se tváří stejně.
