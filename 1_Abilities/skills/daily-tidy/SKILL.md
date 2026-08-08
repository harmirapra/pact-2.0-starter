---
name: daily-tidy
description: >-
  Denní úklidová rutina — spustí pact doctor, projde nové výstupy, aktualizuje
  aktivní projekty a na konci commitne a nabídne push.
  Use when: uživatel řekne "udělej denní úklid", "projdi PACT", "daily tidy",
  "zkontroluj a zálohuj PACT", "co se dnes změnilo", "clean up and commit",
  nebo se blíží konec dne a chce mít jistotu, že nic nezůstalo neuložené.
---

# daily-tidy

Rutina, ne kontrola. Cíl je, aby na konci dne nebylo nic rozdělaného, co jde uzavřít, a nic důležitého, co jen leží v konverzaci a nikde jinde.

## Postup

### 1. `pact doctor`

Spusť a ukaž výstup celý, i `OK` řádky — je to nejrychlejší způsob, jak vidět, jestli se od minule něco nezhoršilo.

- **`FAIL`** — zastav se u něj. Oprav, nebo aspoň vysvětli uživateli, co je rozbité, dřív než pokračuješ dál v rutině.
- **`WARN`** — pokračuj, ale zapamatuj si je pro shrnutí na konci.

### 2. Nové výstupy

Projdi, co za poslední den vzniklo — nové soubory v `0_Projects/`, dokončené kusy práce. Pro každý aktivní projekt s čerstvou změnou:

- Odpovídá `PROJECT.md` a `PRD.md` tomu, co se reálně postavilo? Pokud ne, aktualizuj (povinná retrospektiva z `AGENTS.md`).
- Patří získaná znalost do `architecture.md`? Zapiš rozhodnutí a zdůvodnění, ne jen že se něco změnilo.

Neaktualizuj mlčky — u každé úpravy řekni uživateli jednou větou co a proč.

### 3. Cíle

Krátce se zeptej: *změnilo se dnes něco, co má vliv na `2_Context/goals/goals.md`?* Většinu dní je odpověď ne — nevnucuj úpravu, jen se zeptej.

### 4. Commit

Ukaž `git status` a `git diff` shrnutě (co se změnilo, ne celý diff řádek po řádku, pokud si uživatel nevyžádá víc). Navrhni commit zprávu, která vysvětluje **proč**, ne jen že „aktualizace". Commitni po potvrzení.

### 5. Push

Zeptej se, jestli pushnout — u znalostního obsahu PACTu je to obvykle ano, protože push je záloha (`docs/`, sekce o gitu v `AGENTS.md`). Nepushuj automaticky bez potvrzení, i když je to denní rutina: uživatel mohl mít rozdělanou práci, kterou nechce zveřejnit ještě dnes.

## Kdy tuhle rutinu nepoužívat

- U kódových repozitářů typu `dual-root` — tam platí `git-safe-change` (větev, PR, review), ne přímý commit do `main`.
- Když `pact doctor` na začátku hlásí `FAIL` kvůli tajemství ve verzovaném souboru — to se neuklízí rutinou, to se řeší okamžitě a odděleně.

## Když narazíš na placeholder, který tam nemá být

Pokud `2_Context/` obsahuje `[DOPLNIT]` už déle než pár dní, připomeň to jednou větou a odkaž na `pact-setup` — ale nevynucuj dokončení uprostřed jinak hotové rutiny.
