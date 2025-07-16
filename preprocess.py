#!/usr/bin/env python3
"""
preprocess.py

Command‑line interface for building your Sentinel‑1 stack.
"""

import argparse
import glob
import numpy as np
import rasterio

def load_and_preprocess_tif(path):
    # TODO: open with rasterio, apply your Lee filter + resize to 128x128
    with rasterio.open(path) as src:
        img = src.read(1)
    # e.g., img = lee_filter(img)
    # e.g., img = resize_to_128(img)
    return img

def build_from_tiffs(input_dir, output_npy):
    paths = sorted(glob.glob(f"{input_dir}/*.tif"))
    stack = [load_and_preprocess_tif(p) for p in paths]
    np.save(output_npy, np.stack(stack))
    print(f"Saved {{len(stack)}} images to {{output_npy}}")

def build_from_npy(input_npy, output_npy):
    data = np.load(input_npy, mmap_mode='r')
    # Optionally re-process here
    np.save(output_npy, data)
    print(f"Copied stack from {{input_npy}} to {{output_npy}}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Build Sentinel‑1 .npy stack")
    p.add_argument("--input",  required=True,
                   help="folder of TIFFs or path to .npy stack")
    p.add_argument("--output", required=True,
                   help="path for the output .npy file")
    args = p.parse_args()

    if args.input.lower().endswith(".npy"):
        build_from_npy(args.input, args.output)
    else:
        build_from_tiffs(args.input, args.output)
