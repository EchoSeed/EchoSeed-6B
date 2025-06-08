"""
EchoSeed Loader Script
======================

This script downloads 10 JSONL shard files containing EchoSeed data and merges them into one dataset.
Use it for training, inference, or analysis in any Python environment or Jupyter/Colab notebook.

INSTRUCTIONS:
-------------
1. Replace the `shard_urls` list with the actual URLs where your shard files are hosted.
2. Run this script in your Python environment.
3. The merged dataset will be saved as `echo_merged_1M.jsonl`.

REQUIREMENTS:
-------------
- Python 3.6+
- tqdm
- requests

Install missing packages with:
    pip install tqdm requests
"""

import os
import json
import requests
from tqdm import tqdm

# Directory to store shards
os.makedirs("echo_shards", exist_ok=True)

# TODO: Replace these with your actual URLs
shard_urls = [
    f"https://yourdomain.com/path/echo_shard_{i:02d}.jsonl" for i in range(1, 11)
]

# Download all shard files
def download_shards(urls):
    for url in urls:
        filename = url.split("/")[-1]
        filepath = os.path.join("echo_shards", filename)
        if not os.path.exists(filepath):
            print(f"Downloading {filename}...")
            r = requests.get(url, stream=True)
            with open(filepath, "wb") as f:
                for chunk in tqdm(r.iter_content(chunk_size=8192)):
                    f.write(chunk)
    print("All shards downloaded.")

# Load and combine all entries into a single list
def load_echo_data():
    dataset = []
    for i in range(1, 11):
        shard_path = os.path.join("echo_shards", f"echo_shard_{i:02d}.jsonl")
        with open(shard_path, "r") as f:
            for line in f:
                dataset.append(json.loads(line))
    return dataset

# Save the combined dataset to one .jsonl file
def save_merged(dataset, filename="echo_merged_1M.jsonl"):
    with open(filename, "w") as f:
        for entry in dataset:
            f.write(json.dumps(entry) + "\n")

# Run the full process
if __name__ == "__main__":
    download_shards(shard_urls)
    data = load_echo_data()
    save_merged(data)
    print(f"Loaded {len(data):,} entries into memory.")
