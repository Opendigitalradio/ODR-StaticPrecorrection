import numpy as np
import matplotlib.pyplot as plt
import src.dab_util as du


def calc_signal_sholder_ratio(fft, sampling_rate, debug = False, debug_path="", suffix=""):
    fft_size = fft.shape[0]
    n_sig = (du.freq_to_fft_sample(-du.c["bw"]/2., fft_size, sampling_rate),
             du.freq_to_fft_sample( du.c["bw"]/2., fft_size, sampling_rate))
    sig = np.mean(fft[n_sig[0]:n_sig[1]])

    n_noise = (du.freq_to_fft_sample(-3000000., fft_size, sampling_rate),
               du.freq_to_fft_sample(-2500000, fft_size, sampling_rate))
    noise = np.mean(fft[n_noise[0]:n_noise[1]])

    n_sholder = (du.freq_to_fft_sample(-1500000, fft_size, sampling_rate),
               du.freq_to_fft_sample(-du.c["bw"]/2, fft_size, sampling_rate))
    sholder = np.mean(fft[n_sholder[0]:n_sholder[1]])

    score = -sholder

    if debug == True:
        print(n_sig, n_sholder, n_noise)
        plt.plot(fft)
        plt.plot((n_sig[0], n_sig[1]), (sig, sig), linewidth=5, color='g')
        plt.plot((n_noise[0], n_noise[1]), (noise, noise), linewidth=5, color='r')
        plt.plot((n_sholder[0], n_sholder[1]), (sholder, sholder), linewidth=5, color='y')
        plt.savefig(debug_path + "/" + str(score) + suffix + ".png")
        plt.clf()

    return score
