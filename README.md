# Climate Change & Related Health – Continent Extraction

This repository contains one script to extract:
1) all contributing continents, and
2) leading continents (first and corresponding author addresses)

from a Web of Science Core Collection (WoSCC) plain-text export.

## Input
Export records from WoSCC in plain text format and save as `data.txt`.

## Run
```bash
python script.py --input data.txt --outdir outputs
