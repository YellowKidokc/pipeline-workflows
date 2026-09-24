# Portability Verification

Verified on 2026-09-23 from a copied and renamed station folder.

- The shipped package contained no virtual environment, workspace output, cache, node modules, or build-only source.
- No fixed Windows drive, user-profile, UNC, or station-root path was found in active scripts, configuration, or documentation.
- No filesystem links or reparse points were present.
- `SETUP.bat` created a fresh local virtual environment from the relocated folder.
- TubeScribe and MarkItDown reported installed versions from that relocated environment.
- A real SRT was copied through `IMPORT_TO_DROP.ps1`; its SHA-256 matched the source.
- `CONVERT_FILE.bat` produced Markdown under the relocated folder's own `Workspace`.
- `pip check` reported no broken requirements.

After copying or renaming this folder, run `SETUP.bat`. Machine-specific `.venv` and generated `Workspace` data are intentionally not part of the clean source package.
