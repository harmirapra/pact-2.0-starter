# Stack — agenti a rozšíření

> Manifest toho, čím pracuješ. Vyplňuje se v `pact-setup`, kroku 6, a
> udržuje dovednost `scope-review` (kolize s baseline dovednostmi).
> Tenhle soubor je záznam, ne instalátor — `pact sync` z něj nic
> neinstaluje, jen ho čte `scope-review` a člověk, který se ptá "čím to
> vlastně běží".

## Agenti

Kterými AI agenty s tímhle PACT pracuješ — může jich být víc.

| Agent | Role / kdy ho používáš | Poznámka |
|---|---|---|
| [DOPLNIT] | [DOPLNIT] | [DOPLNIT] |

## Rozšíření (vrstva 2 — viz `docs/VRSTVY.md`)

Pluginy, marketplace rozšíření, hooks, slash commands. Vendor-specific —
fungují jen v jednom nástroji, `1_Abilities/skills/` je nezná.

| Rozšíření | Agent | Co dělá | Kolize s baseline dovedností? |
|---|---|---|---|
| [DOPLNIT] | [DOPLNIT] | [DOPLNIT] | [DOPLNIT: ne / ano — která, a rozhodnutí] |

## Externí nástroje (vrstva 3)

MCP servery, API, SaaS integrace. Částečně přenositelné (MCP je standard),
ale mimo rozsah v1 PACT-2.0.

| Nástroj | K čemu | Poznámka |
|---|---|---|
| [DOPLNIT] | [DOPLNIT] | [DOPLNIT] |

## Rozhodnutí o kolizích

Zapisuje `scope-review` při každé revizi. Formát: datum, dvojice
(dovednost × rozšíření), rozhodnutí, jednořádkové zdůvodnění.

- [DOPLNIT: zatím žádná revize neproběhla]
