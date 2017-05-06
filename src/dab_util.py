import numpy as np
import scipy
import matplotlib.pyplot as plt
import fftconvolve

c = {}
c["bw"]=1536000
c["frame_ms"]=96
c["frame_8192000"]=c["frame_ms"] * 8192
c["frame_2048000"]=c["frame_ms"] * 2048
c["sym_8192000"]=96./76*8192
c["sym_2048000"]=96./76*2048

def calc_fft(signal, fft_size = 65536, sampling_rate = 8192000, plot = False):
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

def crop_signal(signal, n_window = 1000, n_zeros = 120000, debug = False):
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
    signal = signal[max(0,idx_start - n_zeros): min(idx_end + n_zeros, signal.shape[0] -1)]
    return signal

#def fftlag(signal_original, signal_rec):
#    """
#    Efficient way to find lag between two signals
#    Args:
#        signal_original: The signal that has been sent
#        signal_rec: The signal that has been recored
#    """
#    c = np.flipud(scipy.signal.fftconvolve(signal_original,np.flipud(signal_rec)))
#    #plt.plot(c)
#    return np.argmax(c) - signal_original.shape[0] + 1

def fftlag(signal_original, signal_rec, n_upsampling = 1):
    """
    Efficient way to find lag between two signals
    Args:
        signal_original: The signal that has been sent
        signal_rec: The signal that has been recored
    """
    c = np.flipud(fftconvolve.fftconvolve(signal_original,np.flipud(signal_rec), n_upsampling))
    #plt.plot(c)
    return (np.argmax(c) - signal_original.shape[0] + 1)

def get_amp_ratio(ampl_1, ampl_2, a_out_abs, a_in_abs):
    idxs = (a_in_abs > ampl_1) & (a_in_abs < ampl_2)
    ratio = a_out_abs[idxs] / a_in_abs[idxs]
    return ratio.mean(), ratio.var()

def get_phase(ampl_1, ampl_2, a_out, a_in):
    idxs = (np.abs(a_in) > ampl_1) & (np.abs(a_in) < ampl_2)
    ratio = np.angle(a_out[idxs], deg=True) - np.angle(a_in[idxs], deg=True)
    return ratio.mean(), ratio.var()
