<!--
  Šablona PROJECT.md pro `pact new`. Obsahuje dva bloky, jeden pro
  každý typ projektu (single-root / dual-root, viz docs/DUAL-ROOT.md).
  `pact new` vybere podle zvoleného typu jeden blok mezi značkami
  TEMPLATE/​/TEMPLATE, značky i tenhle komentář ve výsledném PROJECT.md
  nezůstanou. Needituj značky ani jména proměnných {{...}}, needituj
  ručně vygenerovaný PROJECT.md — tahle šablona needituje generovaný obsah,
  jen ho vyrábí.
-->
<!-- TEMPLATE:single-root -->
---
name: {{name}}
type: single-root
status: active
---

# {{name}}

[DOPLNIT: popis projektu]

## Otevřené otázky

- [DOPLNIT]
<!-- /TEMPLATE -->
<!-- TEMPLATE:dual-root -->
---
name: {{name}}
type: dual-root
status: active
code:
  path: {{code_path}}
  remote: {{code_remote}}
  visibility: {{code_visibility}}
---

# {{name}}

[DOPLNIT: popis projektu]

## Dual root

Kódová část tohoto projektu není v PACT. Leží v:
{{code_path}}

- Do PACT nikdy nekopíruj kód.
- Do kódového repa nikdy nekopíruj obsah 2_Context/.
- Pokud na tu cestu nedosáhneš, ŘEKNI MI TO a navrhni, jak si v prostředí,
  ve kterém běžíš, rozšířit dosah. NEHÁDEJ obsah.

## Kontext vyšší úrovně

Tento projekt navíc používá:
- [DOPLNIT]

Pokud na ně nedosáhneš, ŘEKNI MI TO. Nepokračuj bez nich.

## Otevřené otázky

- [DOPLNIT]
<!-- /TEMPLATE -->
