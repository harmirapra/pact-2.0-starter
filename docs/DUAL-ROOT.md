# Dual root — typy projektů a vazba na kódový root

## Rozhodovací otázka

`pact new` se ptá:

> *„Bude mít tenhle projekt vlastní repozitář vedle PACTu — protože ho chceš sdílet, zveřejnit, nebo mu dát vlastní život? Nebo zůstane celý uvnitř PACTu?"*

Otázka cílí na to, co v okamžiku zakládání projektu skutečně víš: zda chceš vlastní repozitář kvůli sdílení, zveřejnění nebo samostatnému životu projektu. Smíchat tento rozhodovací signál s jinými vlastnostmi projektu by tě mohlo svést k tomu, že malá utilita skončí ve zbytečném vlastním repu.

## Dva typy

| Typ | Kde žije kód | Repo | Kdy ho zvolit |
|---|---|---|---|
| `single-root` | uvnitř PACTu — `3_Tools/`, nebo přímo ve složce projektu | jedno privátní repo PACTu | nechceš pro projekt vlastní repozitář; celý zůstane uvnitř PACTu |
| `dual-root` | v paralelním rootu vedle PACTu | vlastní, může být public nebo sdílené | chceš projekt zveřejnit, sdílet s někým dalším, nebo mu dát vlastní život |

Uvnitř PACTu se **neptáme, kam přesně kód patří** — platí konvence z `AGENTS.md`: znovupoužitelný nástroj do `3_Tools/`, jinak do složky projektu.

## Co kritérium NENÍ

O typu projektu nerozhoduje:

- velikost projektu,
- jestli je uživatel začátečník,
- jestli kód už existuje — to rozhoduje jen o tom, zda po založení použiješ `pact link`.

## Proč vůbec dva rooty

Kontext a kód mají odlišný životní cyklus:

| | PACT root | Kódové repo |
|---|---|---|
| Kadence změn | pomalá, lidská | rychlá, strojová |
| Jednotka změny | rozhodnutí, znalost | commit, PR, release |
| Historie slouží | tobě za rok | reviewerovi zítra |

Kdyby žily v jednom repu, každé doladění promptu by zašumělo historii kódu a naopak. Odlišný životní cyklus je **důvod**, proč dva rooty existují; rozhodovacím **pravidlem** je, zda projekt dostane vlastní repozitář kvůli sdílení, zveřejnění nebo samostatnému životu.

## `PROJECT.md`

### `single-root`

```yaml
---
name: muj-projekt
type: single-root
status: active
---
```

Blok `code:` chybí.

### `dual-root`

```yaml
---
name: muj-projekt
type: dual-root
status: active
code:
  path: ../../../repos/muj-projekt
  remote: git@github.com:<user>/muj-projekt.git
  visibility: public
---
```

Tělo dokumentu navíc obsahuje standardní blok **„## Dual root"** — je to instrukce pro agenta, ne jen zápis dat:

```markdown
## Dual root

Kódová část tohoto projektu není v PACT. Leží v:
../../../repos/muj-projekt

- Do PACT nikdy nekopíruj kód.
- Do kódového repa nikdy nekopíruj obsah 2_Context/.
- Pokud na tu cestu nedosáhneš, ŘEKNI MI TO a navrhni, jak si v prostředí,
  ve kterém běžíš, rozšířit dosah. NEHÁDEJ obsah.
```

Poslední odrážka je nejcennější: agent, který na kódovou složku nedosáhne, si její obsah typicky domyslí — a ty to poznáš pozdě. Mechanismus rozšíření dosahu (VS Code multi-root workspace, `/add-dir` u CLI agentů…) závisí na tom, čím právě běžíš; `pact link --workspace` umí jeden konkrétní vygenerovat, viz níže.

Pokud projekt navíc čerpá kontext z vyšší úrovně (`2_Context/expertise/…`, konkrétní dovednost), patří k tomu druhý blok, **„## Kontext vyšší úrovně"**, se stejným pravidlem: na co agent nedosáhne, na to se zeptá, nedomýšlí.

## Příkazy

| Příkaz | Co dělá |
|---|---|
| `pact new <nazev>` | založí projekt, zeptá se na typ (a u `dual-root` na viditelnost), vygeneruje `PROJECT.md` a `README.md` |
| `pact link <projekt> [--code-path PATH] [--workspace]` | připojí existující kódový repozitář k projektu typu `dual-root`; ověří, že cesta existuje a je git repozitář; `--workspace` navíc vygeneruje `../workspaces/<projekt>.code-workspace` se dvěma kořeny |
| `pact promote <projekt> [--code-path PATH]` | povýší `single-root` na `dual-root` — změní `type`, doplní blok `code:` a blok „## Dual root" |

`pact link` a `pact promote` nikdy nezakládají kódový repozitář samy — očekávají, že už existuje.

## Založení nového `dual-root` projektu

1. Agent spustí `pact new`; rozhodovací otázku položí CLI a agent ji nekomentuje.
2. Uživatel potvrdí cestu ke kódu.
3. Pokud adresář neexistuje, agent ho smí založit.
4. Agent vypíše `cd <potvrzená-cesta>` a až potom `git init` a případné
   `gh repo create <potvrzené-jméno> --private --source=.`. Příkazy nespustí;
   provede je uživatel.
5. Až je kódové repo hotové, agent ho připojí přes `pact link`.

`pact new` ani `pact link` kódové repo samy nevytvářejí. Založení adresáře je
práce agenta; inicializace gitu zůstává podle L2 na uživateli.

## Cena `single-root`, kterou stojí za to znát

Kód uvnitř PACTu sdílí kořen workspace s kontextem a znalostní částí. V praxi to znamená, že cokoli, co kódový nástroj v tom kořeni očekává — konfigurace CI, `package.json`, buildovací skripty — prosakuje do kořene celého PACT repozitáře, ne jen do složky projektu. Není to důvod proti `single-root`; je to cena, kterou má uživatel platit vědomě, ne ji objevit až za pár měsíců.

## Vědomě mimo rozsah

- Copilot app (desktop) — je repozitářově orientovaný, ne složkový; multi-root se do něj nepřekládá.
- Automatický převod existujících projektů mezi typy jinak než přes `pact promote`.
