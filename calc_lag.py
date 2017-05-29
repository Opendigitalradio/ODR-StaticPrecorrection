from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import re
import sys
from tqdm import tqdm

from glob import glob
from natsort import natsorted
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import src.dab_util as du




tx_paths = natsorted(glob(r'/home/andreas/dab/ODR-StaticPrecorrection/data/received/*_tx_record.iq'))
rx_paths = natsorted(glob(r'/home/andreas/dab/ODR-StaticPrecorrection/data/received/*_rx_record.iq'))

res = []

for tx_path, rx_path in zip(tx_paths, rx_paths):
    s1 = du.fromfile(tx_path)
    s2 = du.fromfile(rx_path)

    res.append({
              '1':du.lag_upsampling(s2, s1, n_up=1),
              '2':du.lag_upsampling(s2, s1, n_up=2),
              '3':du.lag_upsampling(s2, s1, n_up=3),
              '4':du.lag_upsampling(s2, s1, n_up=4),
              '8':du.lag_upsampling(s2, s1, n_up=8),
              '16':du.lag_upsampling(s2, s1, n_up=16),
              '32':du.lag_upsampling(s2, s1, n_up=32),
            })

df = pd.DataFrame(res)
df = df.reindex_axis(sorted(df.columns), axis=1)
print(df)
print(df.describe())

