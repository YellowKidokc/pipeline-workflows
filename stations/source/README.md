# Station Source Mirror

Repo-safe snapshots of station bodies from `X:\Backside\stations`.

This folder is for online prompting and refactoring. It intentionally excludes:

- runtime `INPUT/`, `OUTPUT/`, `ARCHIVE/`, `ERROR/`, `LOGS/`, `REVIEW/`
- generated exports and paper/build output
- virtual environments and dependency folders
- model weights, databases, cassettes, media, archives
- local secrets, credentials, tokens, and real `.env` files

The executable source of truth remains the NAS station path in `stations/STATION_REGISTRY.json`. Changes proposed here must be intentionally ported back to the live station or promoted into this repo's engine layer.
