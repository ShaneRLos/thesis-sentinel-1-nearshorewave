# Sentinel‑1 Thesis

## Setup
```bash
pip install -r requirements.txt

## Sample data
`sample_data/` contains a tiny subset to test locally.  
Full 650 MB stack → Zenodo DOI (coming soon).

## Usage
```bash
python preprocess.py \
  --input sample_data/stack_sample.npy \
  --output results/

