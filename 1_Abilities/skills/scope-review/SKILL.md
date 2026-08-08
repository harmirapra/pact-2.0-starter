---
name: scope-review
description: >-
  Periodická revize toho, na které úrovni rozsahu (uživatelská/repo) má co
  žít, a detekce kolizí mezi baseline dovednostmi a nově nainstalovanými
  pluginy.
  Use when: uživatel řekne "projdi mi rozsah dovedností", "scope review",
  "co by mělo být globální", "nainstaloval jsem plugin, co s tím", "review
  what's on the user level", "check for skill collisions", nebo si po čase
  všimne, že některá dovednost nikdy nevystřelí.
---

# scope-review

Není součástí iniciace (to řeší `pact-setup`, krok 5) — spouští se **periodicky nebo nahodile**, až něco v `1_Abilities/` a `2_Context/` reálně existuje a má historii používání.

**Nic nepřesouvá ani nemaže samo.** Vždy jen navrhne s odůvodněním a čeká na rozhodnutí. Teprve po schválení spusť `pact sync`.

## 1. Projdi inventář

Pro každou dovednost v `1_Abilities/skills/` a každou položku v `2_Context/` navrhni úroveň podle signálů:

| Signál | Návrh |
|---|---|
| používá se ve víc projektech | ↑ uživatelská úroveň |
| užitečné i mimo PACT (třeba při práci nad cizím kódem) | ↑ uživatelská úroveň |
| odkazuje na konkrétní projekt v `0_Projects/` | ↓ projektová úroveň |
| na uživatelské úrovni, ale reálně použito jen v jednom projektu | ↓ zpět do PACT |
| obsahuje osobní nebo citlivý obsah | ✗ nikdy uživatelská úroveň |
| nově nainstalovaný plugin pokrývá stejné území | ⚠️ kolize — viz sekce 3 |

Kontrolní otázka u každého posunu **nahoru**: *chci, aby tohle viděl agent při práci nad cizím (např. firemním) kódem?*

## 2. Nespuštěná dovednost není totéž co nepotřebná

**Kontrolní řádek navíc (zastávka S2):** když dovednost v `1_Abilities/skills/` za sledované období ani jednou nevystřelila, ale uživatel tu samou práci mezitím dělal ručně, problém nemusí být v obsahu dovednosti — může být v jejím `description`. Nespuštěná dovednost dnes vypadá stejně jako nepotřebná, a je snadné ji omylem zahodit.

U každé takové dovednosti se nejdřív zeptej: *dělal jsi tohle nedávno ručně?* Pokud ano, navrhni přepsat `description` (spouštěcí fráze, které by uživatel skutečně použil) dřív, než padne verdikt „zahodit".

## 3. Kolize s pluginy

Runtime arbitráž mezi dovednostmi **není řiditelná** — `SKILL.md` nemá pole pro prioritu ani pořadí. Když nově nainstalovaný plugin pokrývá stejné území jako baseline dovednost v `1_Abilities/skills/`, nezjistíš to za běhu — zjistíš to jen při revizi, tady.

Postup:

1. Projdi `2_Context/stack.md` — co je tam zapsané jako rozšíření agenta (vrstva 2, `docs/VRSTVY.md`).
2. Pro každou dvojici (baseline dovednost, plugin na stejném území) rozhodni s uživatelem:

| Varianta | Kdy dává smysl |
|---|---|
| **Ponechat baseline jako pojistku** | prostředí, kde plugin nemusí být (jiný stroj, banka, jiný agent) — princip P13 |
| **Vyřadit baseline** | plugin je spolehlivě dostupný všude, kde uživatel pracuje |

3. Zapiš rozhodnutí do `2_Context/stack.md`, ne jen do konverzace — jinak se za tři měsíce řeší znovu od nuly.

**Co scope-review neřeší:** kterou dovednost aktivace vybere, když obě existují zároveň. To řídí `AGENTS.md` (kontext se dodává nezávisle na mechanismu, ne dovednost s dovedností) — viz `docs/VRSTVY.md`.

## Výstup

Shrnutí ve tvaru: navržené přesuny nahoru / dolů / kolize k rozhodnutí. Po schválení uživatelem uprav `2_Context/scope.yml` (a `stack.md` u kolizí) a spusť `pact sync`.
