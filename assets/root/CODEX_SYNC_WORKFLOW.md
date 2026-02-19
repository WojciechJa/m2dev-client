# Codex Sync Workflow (WojciechJa + d1str4ught)

Haslo wywolania dla Codex:
`SYNC_D1_KEEP_LOCAL`

Znaczenie:
- Twoj `origin` (WojciechJa) ma zawierac:
  - wszystkie nowe commity z `upstream` (d1str4ught),
  - oraz Twoje lokalne zmiany.
- Przy konfliktach priorytet:
  - zachowac Twoje modyfikacje tam, gdzie jest konflikt,
  - ale recznie domergowac nowe rzeczy z upstream, jesli da sie bez regresji.

Standard krokow:
1. `git fetch origin --prune`
2. `git fetch upstream --prune`
3. `git checkout main`
4. `git pull --ff-only origin main`
5. `git merge upstream/main`
6. Rozwiazanie konfliktow recznie (nie slepe `--ours` dla wszystkiego).
7. Szybki audit po merge:
   - brak markerow konfliktu,
   - brak brakujacych helperow/API po merge,
   - szybki parse skladni `assets/root/*.py`.
8. Commit merge + push na `origin/main`.

Uwagi:
- `assets/root/serverinfo.py` jest lokalnie oznaczony jako `skip-worktree` (nie commitowac prywatnego IP).
- Po testach usuwac/ignorowac `assets/root/__pycache__/`.
