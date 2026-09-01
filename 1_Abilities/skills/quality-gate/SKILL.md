---
name: quality-gate
description: >-
  Nezávislá kontrola hotového výstupu před odevzdáním — proti tvým kritériím kvality,
  tvému tone of voice a proti vymyšleným tvrzením. Vrací PASS nebo NEEDS EDIT
  s konkrétními opravami.
  Use when: uživatel řekne "zkontroluj to", "zkontroluj text", "review", "projdi to
  před odesláním", "je to hotové?", "zpětná vazba na text", "quality gate",
  "check this", "review this before I send it". Použij taky sám od sebe na konci
  delšího workflow, které něco produkuje.
  Nepoužívej na review implementace proti plánu (git diff, RPI cyklus) —
  na to je rpi-review.
---

# Quality gate

Poslední kontrola před tím, než něco odejde ven. Nejsi autor — jsi nezávislý reviewer a tvoje práce je najít, co je špatně, ne pochválit.

## Než začneš: načti kritéria

Kontrolní seznam bez kritérií je k ničemu. Načti v tomhle pořadí:

| Zdroj | Co z něj bereš |
|---|---|
| `2_Context/quality-criteria.md` | vlastní kritéria uživatele — co pro něj znamená hotový výstup |
| `2_Context/identity/tone-of-voice/` | jak má text znít |
| `2_Context/identity/about-me.md` | kdo je autor a v jaké roli text posílá |
| `2_Context/expertise/` | doménová terminologie, jestli je výstup odborný |

**Když `2_Context/quality-criteria.md` neexistuje nebo obsahuje jen `[DOPLNIT]`:** nepředstírej, že kritéria máš. Napiš uživateli jednu větu — *„Tvoje vlastní kritéria kvality nejsou vyplněná, kontroluju jen proti baseline a tone of voice. Chceš je teď doplnit?"* — a pokračuj s baseline částí.

Totéž platí pro `tone-of-voice/`. Bez něj nemůžeš posoudit shodu se stylem; řekni to a tu položku vynech, místo abys ji odhadl.

## Baseline — platí vždy, i bez vyplněných kritérií

Tohle jsou kontroly, které dávají smysl u každého výstupu a agent je sám od sebe nedělá:

1. **Nepodložená tvrzení.** Projdi konkrétní údaje — čísla, jména, data, citace, odkazy. U každého se ptej: *je to ve zdrojích, které jsem měl k dispozici?* Co tam není, označ. Tohle je nejdůležitější kontrola celé dovednosti; vymyšlený, ale věrohodně znějící údaj je nejdražší chyba, kterou AI výstup dělá.
2. **Odpovídá to na položenou otázku?** Text může být dobře napsaný a přitom míjet zadání. Porovnej výstup se zadáním, ne sám se sebou.
3. **Prázdná místa.** Formulace typu „záleží na okolnostech", „je třeba zvážit", „vhodným řešením může být" — místa, kde text vypadá, že něco říká, ale neříká nic.
4. **Chybějící závěr.** Když si výstup říká o rozhodnutí nebo akci, je z něj jasné, co se má stát dál a kdo to má udělat?

## Uživatelská část

Projdi výstup proti každému kritériu z `2_Context/quality-criteria.md` zvlášť a u každého uveď verdikt s odůvodněním. Nezobecňuj do jednoho „splňuje".

## Shoda s tone of voice

Nekontroluj dojem, kontroluj konkrétní pravidla z `tone-of-voice/`. U každého porušení cituj místo v textu.

## Kód a vizuální výstup

Pokud je součástí výstupu kód nebo návrh rozhraní, přidej:

- **Kód:** funguje na uvedených vstupech? ošetřuje chybové stavy? je čitelný za měsíc?
- **Rozhraní:** je zřejmé, co má uživatel udělat? funguje to na malé obrazovce? dá se to ovládat klávesnicí?

Když nemáš jak to ověřit (nemůžeš kód spustit, nevidíš vykreslený výstup), napiš to a označ položku jako neověřenou. Neodhaduj.

## Formát výstupu

```markdown
## Quality gate

**Kontrolováno:** [co to je — e-mail, článek, skript…]
**Verdikt:** PASS / NEEDS EDIT

### Nepodložená tvrzení
[Seznam s citací místa. Když žádná, napiš "žádná nalezena".]

### Vlastní kritéria
| Kritérium | Verdikt | Poznámka |
|---|---|---|

### Tone of voice
[Konkrétní porušení s citací. Nebo "odpovídá".]

### Co opravit
1. [Konkrétní změna — co a proč]
2. …

### Neověřeno
[Co jsi nemohl zkontrolovat a proč.]
```

Když je verdikt NEEDS EDIT a jde o text pod zhruba dvě normostrany, přilož i **opravenou verzi**. U delších textů jen seznam oprav — přepisovat celé je plýtvání a uživatel ztratí přehled, co se změnilo.

## Příklad

**Vstup:** e-mail klientovi s větou *„Podle nedávné studie ušetří firmy s automatizovaným reportingem až 40 % času."*

**Část výstupu:**

```
### Nepodložená tvrzení
- "Podle nedávné studie … až 40 % času" — ve zdrojích, které jsem dostal,
  žádná taková studie není. Buď doplň konkrétní zdroj (autor, rok), nebo větu
  přeformuluj na vlastní zkušenost: "U klientů, se kterými jsme to zaváděli,
  se reporting zkrátil zhruba na polovinu."
```

## Co tahle dovednost nedělá

Nerozhoduje, jestli se výstup odešle. Předloží nález; rozhodnutí je uživatelovo.
