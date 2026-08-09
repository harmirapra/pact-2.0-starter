---
name: plugin-collision-review
description: >-
  Detekce kolizí mezi baseline dovednostmi v 1_Abilities/skills/ a nově
  nainstalovanými rozšířeními agenta (pluginy, marketplace balíčky) —
  se zápisem rozhodnutí do 2_Context/stack.md.
  Use when: uživatel řekne "nainstaloval jsem plugin, koliduje to s něčím",
  "zkontroluj kolize dovedností s pluginy", "check for skill collisions",
  "review plugin overlap", "má tohle smysl mít jako baseline dovednost i s
  tím pluginem", nebo si po instalaci rozšíření agenta všimne, že nějaká
  baseline dovednost přestala vystřelovat.
---

# plugin-collision-review

Spouští se **periodicky nebo nahodile** — nejčastěji po instalaci nového rozšíření agenta (pluginu, marketplace balíčku), kdy je potřeba zjistit, jestli nepokrývá stejné území jako baseline dovednost v `1_Abilities/skills/`.

**Nic nepřesouvá ani nemaže samo.** Vždy jen navrhne s odůvodněním a čeká na rozhodnutí uživatele.

## Kolize s pluginy

Runtime arbitráž mezi dovednostmi **není řiditelná** — `SKILL.md` nemá pole pro prioritu ani pořadí. Když nově nainstalovaný plugin pokrývá stejné území jako baseline dovednost v `1_Abilities/skills/`, nezjistíš to za běhu — zjistíš to jen při revizi, tady.

Postup:

1. Projdi `2_Context/stack.md` — co je tam zapsané jako rozšíření agenta (vrstva 2, `docs/VRSTVY.md`).
2. Pro každou dvojici (baseline dovednost, plugin na stejném území) rozhodni s uživatelem:

| Varianta | Kdy dává smysl |
|---|---|
| **Ponechat baseline jako pojistku** | prostředí, kde plugin nemusí být (jiný stroj, banka, jiný agent) — princip P13 |
| **Vyřadit baseline** | plugin je spolehlivě dostupný všude, kde uživatel pracuje |

3. Zapiš rozhodnutí do `2_Context/stack.md`, ne jen do konverzace — jinak se za tři měsíce řeší znovu od nuly.

**Co `plugin-collision-review` neřeší:** kterou dovednost aktivace vybere, když obě existují zároveň. To řídí `AGENTS.md` (kontext se dodává nezávisle na mechanismu, ne dovednost s dovedností) — viz `docs/VRSTVY.md`.

## Výstup

Shrnutí ve tvaru: zjištěné kolize a doporučení (ponechat / vyřadit) k rozhodnutí. Po schválení uživatelem zapiš rozhodnutí do `2_Context/stack.md`.
