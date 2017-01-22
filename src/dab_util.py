import numpy as np
import scipy
import matplotlib.pyplot as plt

c = {
        "bw":1536000
        }

def calc_fft(signal, fft_size = 1024, sampling_rate = 1, plot = False):
    """returns one numpy array for the frequencies and one for the corresponding fft"""
    signal_spectrum = np.fft.fftshift(np.fft.fft(signal, fft_size))
    freqs = np.fft.fftshift(np.fft.fftfreq(fft_size, d=1./sampling_rate))
    if plot == True:
        plot_freq_spec(freqs, signal_spectrum)
    return freqs, signal_spectrum

def plot_freq_spec(freq, spec = None):
    plt.figure(figsize=(10,5))
    if spec == None:
        plt.plot(freq)
    else:
        plt.plot(freq, np.abs(spec))

def freq_to_fft_sample(freq, fft_size, sampling_rate):
    freq_ratio = 1.0 * fft_size / sampling_rate
    return int(freq * freq_ratio + fft_size / 2)

def crop_signal(signal, n_window = 1000, n_zeros = 1000, debug = False):
    #signal = signal[-10:-1]
    mag = abs(signal)
    window = np.ones(n_window) / float(n_window)
    mag = scipy.signal.convolve(window, mag)
    mag = scipy.signal.convolve(window, mag)
    thr = 0.05 * np.max(mag)
    idx_start = np.argmax(mag > thr)
    idx_end = mag.shape[0] - np.argmax(np.flipud(mag > thr))
    if debug:
        plt.plot(mag < thr)
        plt.plot((idx_start,idx_start), (0,0.1), color='g', linewidth=2)
        plt.plot((idx_end,idx_end), (0,0.1), color='r', linewidth=2)
    signal = signal[idx_start - n_zeros: idx_end + n_zeros]
    return signal
