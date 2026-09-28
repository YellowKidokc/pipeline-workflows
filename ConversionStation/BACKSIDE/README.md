# ConversionStation Backside

This folder contains the technical and record-keeping side of the station.
Ordinary use should happen through the two batch files at the ConversionStation root.

- `PRESERVED_ORIGINALS`: content-addressed copies of every processed source.
- `RECEIPTS`: one JSON receipt per unique source hash.
- `LOGS`: one run-level JSON record for every button run.
- `STATE`: replaceable internal conversion state.
- `CONFIG`: local configuration.
- `ENGINES`: reserved home for wrapped conversion engines.
- `SYSTEM`: reserved home for system support files.

The station is additive: it does not move, delete, or overwrite source files.
