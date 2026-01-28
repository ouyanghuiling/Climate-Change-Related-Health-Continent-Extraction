# Climate Change & Related Health – Continent Extraction

This repository contains one script to extract:
1) All contributing continents, and
2) Leading continents: the continent(s) of the first author (i.e., the author listed first, or the first address when author–address matching was not explicit) and/or the corresponding author(s).

from a Web of Science Core Collection (WoSCC) plain-text export.

## Input
Export records from WoSCC in plain text format and save as `data.txt`.

## Run
```bash
python script.py --input data.txt --outdir outputs
