# Sentinel‑1 Thesis

## Setup
```bash
pip install -r requirements.txt

## Sample data
`sample_data/` contains a tiny subset to test locally.  
Full 650 MB stack → Zenodo DOI (coming soon).

## Data

Full preprocessed stack (688.78 MB) on Zenodo:  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15982289.svg)](https://doi.org/10.5281/zenodo.15982289)


## Usage
```bash
python preprocess.py \
  --input sample_data/stack_sample.npy \
  --output results/

