#!/usr/bin/env python3
"""
preprocess.py

Build a processed Sentinel‑1 .npy stack by Lee‑filtering and resizing each TIFF.
"""

import argparse
import glob
import numpy as np
import rasterio
import cv2
from scipy.ndimage import uniform_filter

def lee_filter(img, size=3):
    img_mean      = uniform_filter(img, size)
    img_sqr_mean  = uniform_filter(img**2, size)
    img_variance  = img_sqr_mean - img_mean**2
    overall_var   = np.var(img)
    weights       = img_variance / (img_variance + overall_var)
    return img_mean + weights * (img - img_mean)

def load_and_preprocess_tif(path, size=3, target_size=(128, 128)):
    with rasterio.open(path) as src:
        sar = src.read(1, masked=True)

    # 1) Lee filter
    filt = lee_filter(sar.data, size=size)
    filt = np.ma.array(filt, mask=sar.mask, fill_value=np.nan)
    if np.isnan(filt).any():
        print(f"Skipping {path} (NaNs present)")
        return None

    # 2) Normalize
    mn, mx = filt.min(), filt.max()
    norm   = (filt - mn) / (mx - mn)

    # 3) Resize
    resized = cv2.resize(norm.filled(), target_size, interpolation=cv2.INTER_AREA)
    return resized

def build_from_tiffs(input_dir, output_npy):
    paths = sorted(glob.glob(f"{input_dir}/*.tif"))
    stack = []
    for p in paths:
        img = load_and_preprocess_tif(p)
        if img is not None:
            stack.append(img)
    np.save(output_npy, np.stack(stack))
    print(f"Saved {len(stack)} images to {output_npy}")

def build_from_npy(input_npy, output_npy):
    data = np.load(input_npy, mmap_mode='r')
    # if you want to re-filter/rescale, you could loop here
    np.save(output_npy, data)
    print(f"Copied stack from {input_npy} to {output_npy}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Build a Lee‑filtered, resized Sentinel‑1 .npy stack"
    )
    p.add_argument("--input",  required=True,
                   help="Folder of TIFFs or path to an existing .npy stack")
    p.add_argument("--output", required=True,
                   help="Path for the output .npy file")
    args = p.parse_args()

    if args.input.lower().endswith(".npy"):
        build_from_npy(args.input, args.output)
    else:
        build_from_tiffs(args.input, args.output)
