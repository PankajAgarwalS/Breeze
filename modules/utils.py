# modules/utils.py

import pandas as pd
import os
from tqdm import tqdm

def save_to_csv(data, path, filename):
    """Saves a DataFrame to a CSV file."""
    if not os.path.exists(path):
        os.makedirs(path)
    data.to_csv(os.path.join(path, filename), index=False)
    print(f"Data saved to {os.path.join(path, filename)}")

def load_from_csv(path, filename):
    """Loads a DataFrame from a CSV file."""
    return pd.read_csv(os.path.join(path, filename))

class TqdmUpTo(tqdm):
    """Provides progress bar for downloads."""
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)
