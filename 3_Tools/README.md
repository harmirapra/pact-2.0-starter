# 3_Tools

CLI a znovupoužitelné nástroje pro tento PACT workspace.

- `bin/pact` — hlavní CLI (`sync`, `registry`, `new`, `link`, `promote`, `doctor`). Python 3.9+, nula externích závislostí. Kontrakty jsou zdokumentované v [`../docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md). `sync` i `registry` podporují `--dry-run` (vypíše plánované operace, nic nezapisuje) — užitečné před prvním spuštěním na cizím stroji.
- `tests/` — `unittest` sada (`python3 -m unittest discover 3_Tools/tests`). `tests/fixtures/fresh/` a `tests/fixtures/filled/` slouží jen `pact doctor` testům — `filled/` obsahuje vymyšlenou testovací personu, nikdy ne reálný obsah.
