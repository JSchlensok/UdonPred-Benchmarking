[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15914315.svg)](https://doi.org/10.5281/zenodo.15914315)


This repository contains the code used to produce data and figures for [UdonPred](https://github.com/JSchlensok/udonpred).

Please note that it is still under active development.

**Getting started**
1. Clone repository
2. `uv venv && uv sync`
3. Download data and SOTA method results from [Zenodo](https://doi.org/10.5281/zenodo.15914315) and unzip
4. Run required notebooks in `notebooks/evaluation` (`Parse CAID3 predictions.ipynb`, `Parse TriZOD predictions.ipynb`, `Calculate per-protein stats.ipynb`). To add additional methods:
    - parse their predictions in the parsing notebooks using the provided utility methods
    - adjust the `METHODS` variable in the `udonpred_benchmarking.constants` module as necessary
5. Reproduce plots using notebooks in `notebooks/plots`
