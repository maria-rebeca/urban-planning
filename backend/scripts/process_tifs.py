import rasterio
import numpy as np
import pandas as pd
import os
import sys

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
lst_path = os.path.join(current_dir, 'lst.tif')
lu_path = os.path.join(current_dir, 'landuse.tif')

if not os.path.exists(lst_path) or not os.path.exists(lu_path):
    print("❌ Error: Tiff files not found. Run download_maps.py first.")
    sys.exit(1)

print("⚙️ Loading Maps...")
with rasterio.open(lst_path) as src_lst:
    lst_data = src_lst.read(1) # Read first band
    profile = src_lst.profile

with rasterio.open(lu_path) as src_lu:
    lu_data = src_lu.read(1)

# Ensure shapes match
if lst_data.shape != lu_data.shape:
    print("❌ Error: Map sizes do not match!")
    sys.exit(1)

# --- CONFIGURATION ---
PIXEL_SIZE = 30 # meters (from download script)
GRID_SIZE = 1000 # meters (1km)

# Calculate how many pixels make up 1km
# 1000m / 30m = 33.33 pixels. We round to 33.
window_px = int(GRID_SIZE / PIXEL_SIZE)

print(f"📏 Grid Config: 1km = {window_px} x {window_px} pixels")

rows, cols = lst_data.shape
dataset = []

print("🧮 Scanning Grid...")

# Loop through the image in 33-pixel jumps
for r in range(0, rows, window_px):
    for c in range(0, cols, window_px):
        # Extract the window (chunk)
        lst_window = lst_data[r:r+window_px, c:c+window_px]
        lu_window = lu_data[r:r+window_px, c:c+window_px]
        
        # Skip incomplete chunks at the edge
        if lst_window.shape[0] < window_px or lst_window.shape[1] < window_px:
            continue

        # 1. Get Temperature
        # Filter out -999 (No Data)
        valid_temps = lst_window[lst_window > -100]
        
        if valid_temps.size == 0:
            continue # Skip empty ocean/border chunks
        
        mean_temp = np.mean(valid_temps)

        # 2. Get Land Use Histogram
        # Flatten the 2D window to 1D array
        lu_flat = lu_window.flatten()
        # Remove 0s (Empty/No Data)
        lu_flat = lu_flat[lu_flat != 0]
        
        if lu_flat.size == 0:
            continue

        # Count frequencies
        unique, counts = np.unique(lu_flat, return_counts=True)
        total_pixels = lu_flat.size
        
        # Build the row
        row_data = {'target_temp': round(mean_temp, 2)}
        
        for code, count in zip(unique, counts):
            percent = (count / total_pixels) * 100
            row_data[f"pct_{int(code)}"] = round(percent, 2)
            
        dataset.append(row_data)

# --- Save ---
print(f"📊 Processed {len(dataset)} grid cells.")
df = pd.DataFrame(dataset).fillna(0)

output_file = os.path.join(current_dir, 'final_training_data.csv')
df.to_csv(output_file, index=False)

print(f"✅ Success! Saved to: {output_file}")
print("Preview:")
print(df.head())