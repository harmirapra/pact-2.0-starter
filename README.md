# PACT-2.0

Osobní AI workspace, nezávislý na konkrétním coding agentovi. Kontext,
dovednosti a znalostní část projektů — kód žije v samostatných repozitářích
(viz `docs/DUAL-ROOT.md`).

## Rychlý start

```
git clone https://github.com/harmirapra/pact-2.0-starter.git ~/muj-pact
cd ~/muj-pact
git remote remove origin
```

Název `muj-pact` je jen příklad — přejmenuj podle potřeby. `~/muj-pact`
je cesta vztažená k tvému domovskému adresáři, funguje bez ohledu na
to, odkud příkaz spouštíš. Místo toho můžeš zadat i plnou cestu
k požadovanému cílovému adresáři, např. `/Users/tvoje-jmeno/Projects/muj-pact`.
Cílovou složku git vytvoří, pokud ještě neexistuje; pokud existuje,
musí být prázdná — jinak klonování selže.

Krok `git remote remove origin` je důležitý: odpojí tvou instanci od
šablony, ze které vznikla. Bez něj by `git push` nebo jiná síťová
operace omylem mířila do repozitáře šablony, ne do tvého vlastního.
Pokud chceš svou instanci zálohovat nebo sdílet, založ si vlastní
remote repozitář a připoj ho zvlášť (`git remote add origin <tvoje-url>`).

Teď spusť svého AI agenta nad touhle novou složkou — ať už otevřením
nové session ve složce `muj-pact`, nebo spuštěním agenta přímo v ní.
Pak mu řekni: *„pomoz mi nastavit tento pact"*.

Kdykoli později se můžeš zeptat: *„pověz mi, jak používat tento pact"*.
Příkazy pod tím obslouží agent — ty popisuješ, co potřebuješ.

### Doporučení: model a tier

PACT-2.0 funguje s jakýmkoli LLM modelem. **Kvalita zážitku závisí na tieru modelu**, kterým agenta provozuješ:

- **Vyšší tier** (např. Claude 3.5 Sonnet se středním reasoning, GPT-4, atd.) — vede dialog, klade otázky, text je přirozený
- **Nižší tier** (auto, free tier, ekonomický režim) — funkčnost zůstane, ale wizard bude méně interaktivní a text může být strojovější

To není vada šablony — je to vlastnost modelu. Když volíš nižší tier pro úsporu usage, očekávej **kratší konverzace a nižší kvalitu textu**, nikoli rozlomení funkčnosti. Podrobně viz `docs/ARCHITECTURE.md`, sekce „Vědomá omezení".

## Struktura

- `0_Projects/` — CO dělám (znalostní část projektů)
- `1_Abilities/` — JAK to udělat (dovednosti, formát `SKILL.md`)
- `2_Context/` — KDO jsem (identita, styl, cíle, stack)
- `3_Tools/` — ČÍM to udělat (CLI, skripty)

Podrobně viz `AGENTS.md` a `docs/`.

## Původ

PACT-2.0 vychází z frameworku **PACT** (Projects · Agents · Context · Tools),
který vytvořil Filip Dřímalka (nowork.ai) — původní repo:
https://github.com/nowork-ai/pact-starter

Kódové jméno téhle větve je **PACT-Endur**, motto **„Build to endure!"**

Není to jen ozdoba. Každé zásadní rozhodnutí v PACT-2.0 je rozhodnutí
o trvanlivosti: otevřené standardy místo formátu jednoho nástroje,
kanonický zdroj a generované adaptéry místo ruční údržby, oddělené kořeny
pro kontext a kód, aby ani jedna historie nezašuměla tu druhou.
Cílem není framework, který je nejchytřejší dnes, ale ten, který bude
fungovat i po výměně nástroje pod ním.

Akronym se posunul: **A** znamená **Abilities**, ne Agents. Důvod je v
`docs/ARCHITECTURE.md`.

## Evoluce od pact-starteru

Zajímá tě, **jak a proč** se PACT-2.0 liší od původní šablony?
Není to jen seznam změn — jde o architektonická rozhodnutí, jejich rizika
a tradeoffy.

Čti `docs/EVOLUCE-OD-STARTERU.md` — vysvětluje:

- **Opravy chyb**, které starter dělal tiše (automatické syncing, falešné alarmy)
- **Standardizace** — transition z Cursor-specifických formátů na otevřené standardy
  (AGENTS.md, SKILL.md)
- **Architektonické změny** — dual root, tříúrovňový model, RPI pipeline
- **Filosofické posuny** — vendor neutralita a princip „doplňuj, nesoutěž"
- **Integrované nástroje pro zdraví PACTu** — `pact sync` (generování adaptérů),
  `pact doctor` (diagnostika OK/WARN/FAIL), `pact registry` (přehled dovedností
  aktuální), `daily-tidy` (denní rutina: doctor + úklid + commit) a
  `plugin-collision-review` (kolize baseline dovedností s pluginy)
- **Vědomá omezení** — co stojí na instrukci místo záruky, co se teprve
  ověřuje v praxi
