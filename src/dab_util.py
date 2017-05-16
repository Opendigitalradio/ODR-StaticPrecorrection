import numpy as np
import scipy
import matplotlib.pyplot as plt
import fftconvolve
import src.dabconst as dabconst
from scipy import signal

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

#def fftlag(sig_orig, sig_rec):
#    """
#    Efficient way to find lag between two signals
#    Args:
#        sig_orig: The signal that has been sent
#        sig_rec: The signal that has been recored
#    """
#    c = np.flipud(scipy.signal.fftconvolve(sig_orig,np.flipud(sig_rec)))
#    #plt.plot(c)
#    return np.argmax(c) - sig_orig.shape[0] + 1

def lag(sig_orig, sig_rec):
    """
    Find lag between two signals
    Args:
        sig_orig: The signal that has been sent
        sig_rec: The signal that has been recored
    """
    off = sig_rec.shape[0]
    c = signal.correlate(sig_orig, sig_rec)
    return np.argmax(c) - off + 1

def lag_upsampling(sig_orig, sig_rec, n_up):
    sig_orig_up = signal.resample(sig_orig, sig_orig.shape[0] * n_up)
    sig_rec_up  = signal.resample(sig_rec, sig_rec.shape[0] * n_up)
    l = lag(sig_orig_up, sig_rec_up)
    l_orig = float(l) / n_up
    return l_orig

def fftlag(sig_orig, sig_rec, n_upsampling = 1):
    """
    Efficient way to find lag between two signals
    Args:
        sig_orig: The signal that has been sent
        sig_rec: The signal that has been recored
    """
    c = np.flipud(fftconvolve.fftconvolve(sig_orig,np.flipud(sig_rec), n_upsampling))
    #plt.plot(c)
    return (np.argmax(c) - sig_orig.shape[0] + 1)

def get_amp_ratio(ampl_1, ampl_2, a_out_abs, a_in_abs):
    idxs = (a_in_abs > ampl_1) & (a_in_abs < ampl_2)
    ratio = a_out_abs[idxs] / a_in_abs[idxs]
    return ratio.mean(), ratio.var()

def get_phase(ampl_1, ampl_2, a_out, a_in):
    idxs = (np.abs(a_in) > ampl_1) & (np.abs(a_in) < ampl_2)
    ratio = np.angle(a_out[idxs], deg=True) - np.angle(a_in[idxs], deg=True)
    return ratio.mean(), ratio.var()

def get_transmission_frame_indices(n_frames, offset, rate = 2048000):
    tm1 = dabconst.tm1(rate)
    indices = [tm1.S_F * i + offset for i in range(n_frames)]
    return indices

def fromfile(filename, offset, length):
    return np.memmap(filename, dtype=np.complex64, mode='r', offset=64/8*offset, shape=length)
