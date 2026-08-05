# Command contract

Run from the standalone project root.

```powershell
$cli = 'Workspace/77_Стандарт_iRidi/tooling/standard_book.py'
$python = '.venv/Scripts/python.exe'
```

## Capture and migrate

`capture-google` is read-only and writes an immutable local baseline. A repeated `--force` run reuses verified images and retries only missing downloads.

```powershell
& 'C:/AI/mcp-google/.venv/Scripts/python.exe' $cli capture-google --document-id <id> --output 'Workspace/77_Стандарт_iRidi/baseline-private'
& $python $cli inventory --baseline <revision-directory> --output <inventory.json>
& $python $cli extract --baseline <revision-directory> --source-dir 'Workspace/77_Стандарт_iRidi/standard-src'
```

Use `extract --force` only for an explicitly approved regeneration of the imported baseline tree. It is not an editorial merge command.

## Validate and build

```powershell
& $python $cli validate --source-dir 'Workspace/77_Стандарт_iRidi/standard-src' --output <validation.json>
& $python $cli build --source-dir 'Workspace/77_Стандарт_iRidi/standard-src' --output-dir <legacy-output> --profile legacy-fidelity --format all
& $python $cli build --source-dir 'Workspace/77_Стандарт_iRidi/standard-src' --output-dir <normalized-output> --profile standard-normalized --format all
& $python $cli index --source-dir 'Workspace/77_Стандарт_iRidi/standard-src' --output-dir <package-output> --release <version-or-working-label>
```

## Query and audit

```powershell
& $python $cli query --package-dir <package-output> --text <question> --audience integrator --job select
& $python $cli audit --package-dir <package-output> --input <project.yaml>
```

Query results must cite UIDs. A gap must not be filled by agent invention. Audit exit code `3` means `needs_input`, which is expected before reviewed typed rules exist.
