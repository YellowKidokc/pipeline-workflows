# Codex prompt — portable front folders

Use this prompt on the Windows drive that contains the real API folders. The
repository is only a reference: Git does not preserve the empty folders in the
operator's local sketch.

## Objective

Reorganize the API workspace into a simple front-folder layout without deleting
or overwriting any source file. There must be one shared engine rather than a
copy of the engine inside every API.

## Authoritative inventory

Use the operator's local **CODEX sketch only to discover the APIs and their
names**. Do not reproduce the sketch's internal directory structure. Discover
all numbered API folders (`000_*`, `001_*`, and so on) from the drive rather
than assuming a fixed count or hard-coding the list.

## Required final layout

The main folder may show only:

- every numbered API folder, ordered by its three-digit number;
- `ONE_MENU.bat`;
- `SETUP.bat`; and
- the hidden `_system` folder.

`_system` contains the single shared implementation of:

1. the relay;
2. the menu; and
3. the parallel runner.

Do not leave duplicate engine implementations in individual API folders.

Every numbered API folder contains only four front items:

```text
INBOX/
OUTBOX/
<API launcher or launchers>
BACKSIDE/
```

Treat the launchers discovered in the local CODEX sketch as authoritative; do
not invent launcher names from this repository. `BACKSIDE` holds only that
API's private support material and delegates shared relay, menu, and parallel
work to `_system`; it is not a private copy of the shared engine.

The only exception is `000_QUICK_CALL`. It remains the self-contained folder
that the operator copies elsewhere, so it has no `BACKSIDE`. Do not make Quick
Call depend on files outside its copied folder.

## Inbox contract

Use `02_GROUP` as the third current inbox lane. Preserve compatibility by also
reading an existing legacy `02_GENERAL` lane; do not rename, move, or delete its
contents automatically.

## Cross-API input

An API normally reads its own `INBOX`. It must also accept another API's
`OUTBOX` as its input without copying the files. Support this from every API
launcher with:

```console
RUN.bat --from 052
```

Resolve `052` to the numbered API folder whose number is `052`, and use that
folder's `OUTBOX` as the read-only input source. Reject an unknown, ambiguous,
or malformed number with a clear message. Never consume, move, rename, or
modify files in an upstream API's `OUTBOX`.

## Mandatory planning gate

**Do not move or create the production layout on the first pass.** First inspect
the drive and write a plan that lists, for every discovered API:

- its three-digit number;
- its name;
- its current path;
- its proposed numbered folder name;
- each launcher found and the launcher that will remain at the front; and
- any collision, ambiguity, missing launcher, or special handling required.

The plan must also identify the proposed locations of `ONE_MENU.bat`,
`SETUP.bat`, and `_system`, explain the `--from NNN` resolution, and explicitly
list every file operation that would be performed. Classify operations as
`CREATE`, `COPY`, or `MOVE`; there must be no `DELETE` operation.

After writing the plan, print its path and a concise summary, then **stop and
wait for the operator's explicit approval**. Approval of this prompt is not
approval of the generated plan. Do not infer approval from silence.

## Execution rules after approval

1. Never delete anything.
2. Never overwrite an existing file. Treat identical files as already present;
   report differing files as conflicts and leave both untouched.
3. Preserve originals while assembling and validating the new layout. If a
   move is approved, perform it only after its destination copy is verified.
4. Keep runtime state and logs out of the visible front folders and under the
   shared `_system` structure.
5. Generate launchers from one shared template so all APIs support the same
   arguments, including `--from NNN`.
6. Make `SETUP.bat` idempotent: repeated runs must be safe.
7. Make menu ordering numeric, not lexicographic by API name.
8. Quote every Windows path and support spaces in the workspace path.
9. Return nonzero exit codes for setup, resolution, relay, or API failures.
10. Record an operation manifest with source, destination, SHA-256, action,
    status, and timestamp for every copied or moved file.

## Validation before reporting completion

Verify and report that:

- the main folder contains only the permitted numbered folders and three shared
  entries;
- each normal API front folder contains only its inbox, outbox, discovered
  launcher set, and `BACKSIDE`;
- `000_QUICK_CALL` is self-contained and has no `BACKSIDE`;
- only one relay, menu implementation, and parallel-runner implementation exist;
- `RUN.bat` works with its own `INBOX` and with `--from NNN`;
- a legacy `02_GENERAL` lane is readable while `02_GROUP` is the current lane;
- filenames containing spaces are handled correctly;
- setup can run twice without changing valid results; and
- every original can be accounted for by the operation manifest.

If any validation fails, stop, preserve all files, and report the failure and
recovery steps. Do not call a partial layout complete.
