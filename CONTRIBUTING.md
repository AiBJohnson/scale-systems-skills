# Contributing

Small, testable corrections are welcome.

## Before opening a change

1. Do not include real customer data, secrets or proprietary business material.
2. Use or extend the synthetic fixtures under `plugins/solopreneur-starter/examples/`.
3. Keep every skill fail-closed: missing facts are reported, not invented.
4. Keep file writes local, run-specific and collision-safe.
5. Do not add sending, publishing, purchasing, deletion or money-moving behavior.
6. Preserve the MIT license notice for public files.

## Validate locally

From the repository root:

```sh
python3 scripts/validate_repo.py
claude plugin validate . --strict
claude plugin validate plugins/solopreneur-starter --strict
```

The two `claude plugin validate` commands are optional for contributors without Claude Code installed; CI runs the repository-owned checks without them.

## Pull requests

Explain the user problem, the behavioral change and how you tested it. Update the expected-output fixture when calculations or safety classifications change. Documentation and examples must match the files actually shipped.
