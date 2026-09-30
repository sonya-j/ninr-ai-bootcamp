# Data directory

`raw/uci_diabetes_296/` contains the checksum-pinned official UCI ZIP, the two files extracted byte-for-byte from it, the UCI API metadata record, and the original article’s full-text XML from NIH PubMed Central. Preparation never edits these files.

`processed/diabetes_130_hospitals_participant.csv` is the reproducible 5,000-row, 26-variable participant derivative. It is rebuilt by `python pipeline.py prepare` and checked by `python pipeline.py validate`.

See `metadata/provenance.json` for URLs, access date, version, hashes, transformations, dependencies, and weighting status. See `metadata/missing_values.csv` for raw missing/unavailable codes and `metadata/data_dictionary.csv` for definitions.
