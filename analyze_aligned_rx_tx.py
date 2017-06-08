"""
Generate analytic plots from aligned TX/RX recordings.
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import src.dab_util as du
import scipy.stats as st
from sklearn.neighbors import KernelDensity
import os

SCATTER_SIZE = 0.0001

def kde2D(x, y, bandwidth, xbins=256j, ybins=256j, **kwargs):
    xx, yy = np.mgrid[x.min():x.max():xbins,
             y.min():y.max():ybins]

    xy_sample = np.vstack([yy.ravel(), xx.ravel()]).T
    xy_train  = np.vstack([y, x]).T

    kde_skl = KernelDensity(bandwidth=bandwidth, **kwargs)
    kde_skl.fit(xy_train)

    z = np.exp(kde_skl.score_samples(xy_sample))
    return xx, yy, np.reshape(z, xx.shape)

def plot_density(x, y, scatter=False, path=None):
    x = np.abs(x)
    y = np.abs(y)

    x = x - np.min(x)
    x = x / np.max(x)
    y = y - np.min(y)
    y = y / np.max(y)

    max_val = max(np.max(x), np.max(y))
    min_val = max(np.min(x), np.min(y))

    xx, yy, zz = kde2D(x, y, (max_val - min_val) * 0.01)
    plt.pcolormesh(xx, yy, zz)

    plt.xlabel("Normalized Absolute TX Amplitude")
    plt.ylabel("Normalized Absolute RX Amplitude")

    plt.savefig(path)

def scatter(x_pos, y_pos, x_neg, y_neg, path=None):
    x_pos, y_pos, x_neg, y_neg = np.abs(x_pos), np.abs(y_pos), np.abs(x_neg), np.abs(y_neg)
    plt.scatter(x_pos, y_pos, s=SCATTER_SIZE, facecolor='blue', label="Positive TX/RX")
    plt.scatter(x_neg, y_neg, s=SCATTER_SIZE, facecolor='red',  label="Negative TX/RX")
    plt.xlabel("Absolute TX Amplitude")
    plt.ylabel("Absolute RX Amplitude")
    plt.legend()
    plt.savefig(path)
    plt.clf()

def scatter_phase(x_pos, y_pos, x_neg, y_neg, path=None):
    x_pos_abs = np.abs(x_pos)
    x_neg_abs = np.abs(x_neg)

    phase_diff_pos = np.angle(x_pos, deg=True) - np.angle(y_pos, deg=True)
    phase_diff_neg = np.angle(x_neg, deg=True) - np.angle(y_neg, deg=True)

    phase_diff_pos = np.mod(phase_diff_pos, 180)
    phase_diff_neg = np.mod(phase_diff_neg, 180)

    plt.scatter(x_pos_abs, phase_diff_pos, s=SCATTER_SIZE, facecolor='blue', label="Positive TX/RX")
    plt.scatter(x_neg_abs, phase_diff_neg, s=SCATTER_SIZE, facecolor='red', label="Negative TX/TX")

    plt.ylabel("Phase difference")
    plt.xlabel("Absolute Amplitude")
    plt.legend()

    plt.savefig(path)
    plt.clf()

def plot_time(rx_rec, tx_rec, path=None, samples=256):
    plt.plot(np.angle(rx_rec[:256]), c='blue', label="RX")
    plt.plot(np.angle(tx_rec[:256]), c='red',  label="TX")
    plt.ylabel("Phase")
    plt.xlabel("Sample")
    plt.savefig(path)
    plt.clf()

def main():
    if not os.path.isdir(FLAGS.out_dir):
        os.makedirs(FLAGS.out_dir)

    rx_rec = du.fromfile(filename=FLAGS.rx_path)
    tx_rec = du.fromfile(filename=FLAGS.tx_path)

    sel_pos = (rx_rec > 0) & (tx_rec > 0)
    rx_rec_pos = rx_rec[sel_pos]
    tx_rec_pos = tx_rec[sel_pos]


    sel_pos = (rx_rec < 0) & (tx_rec < 0)
    rx_rec_neg = rx_rec[sel_pos]
    tx_rec_neg = tx_rec[sel_pos]

    scatter(tx_rec_pos, rx_rec_pos, tx_rec_neg, rx_rec_neg, path=FLAGS.out_dir + '/am_am_scatter.pdf')
    scatter_phase(tx_rec_pos, rx_rec_pos, tx_rec_neg, rx_rec_neg, path=FLAGS.out_dir + '/am_pm_pos_scatter.pdf')

    plot_time(rx_rec, tx_rec, path=FLAGS.out_dir + '/phase_over_time.pdf')

    plot_density(tx_rec_pos, rx_rec_pos, path=FLAGS.out_dir + '/am_am_pos.pdf')
    plot_density(tx_rec_neg, rx_rec_neg, path=FLAGS.out_dir + '/am_am_neg.pdf')

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--rx_path',
      type=str,
      default='/tmp/record/2_rx_record.iq',
      help="Path to complex64 rx recording"
  )
  parser.add_argument(
      '--tx_path',
      type=str,
      default='/tmp/record/2_tx_record.iq',
      help="Path to complex64 tx recording"
  )
  parser.add_argument(
      '--out_dir',
      type=str,
      default='/tmp/analyze_aligned_rx_tx',
      help="Output path"
  )
  FLAGS, unparsed = parser.parse_known_args()

  main()
