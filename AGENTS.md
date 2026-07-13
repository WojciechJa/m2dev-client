# AGENTS.md — classic m2dev client runtime

Read `H:\m2dev-client\AGENTS.md` and
`H:\m2dev-client\m2dev-docs\docs\specifications\development-workflow.md` first.

## Scope and authority

- This repository owns Python UI/runtime scripts, client configuration, packs,
  locale, proto outputs and original client assets.
- Classic C++ behavior and Python bindings belong to `m2dev-client-src-main`.
- This asset tree is the original reference for UE5 import/parity; generated UE5
  assets do not replace it as source evidence.

## Working rules

- The worktree contains many binary and generated user changes. Never bulk-stage,
  repack, convert or normalize assets outside the requested scope.
- Trace Python UI events to the corresponding C++ binding and server state before
  changing presentation logic.
- Keep locale keys, UI script paths, pack roots and case sensitivity compatible
  with the classic runtime loader.
- Proto changes must originate from verified server inputs and be regenerated for
  every affected locale; do not hand-edit packed proto output.
- GR2/DDS/MSA/MSM changes require source-path provenance and tests in classic and,
  when relevant, the UE5 import pipeline.

## Validation

```powershell
Set-Location assets
python pack.py root
# Use `python pack.py --all` only when the requested scope requires a full repack.
```

- Run Python syntax/import checks appropriate for the embedded client Python.
- Rebuild only affected pack/proto outputs with the repository tools. `pack.py`
  requires the matching `PackMaker.exe`.
- Launch the matching client executable and inspect `syserr.txt` and visual flow.
- For asset/data changes verify both classic loading and UE5 parity/import.

Use an atomic repository-local commit linked to the shared WORKLOG ID.
