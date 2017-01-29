import numpy as np
import matplotlib.pyplot as plt

def gen_single_tone_with_silence(path = "./input.dat", n_periods=100, predist = None, par = None, debug = False):
    period = 128
    length = period * n_periods * 3

    t = np.arange(0,length / 3)
    sig = np.zeros(length, dtype=np.complex64)
    sig[length/3:length*2/3] = np.exp(t * 2j * np.pi * 1./period)
    #sin1 = np.cos(t * np.pi * 1./period)

    if predist is None:
        res = sig
    else:
        res = predist(sig, par)

    res = res / np.max(res) * 0.95

    res = res.astype(np.complex64)
    res.tofile(path)

    a_load = np.fromfile(path, dtype=np.complex64)
    assert(np.isclose(a_load, res).all()), "Inconsistent stored file"

    if debug == True:
        plt.plot(np.abs(np.concatenate((a_load, a_load))))
        plt.savefig(path + ".png")
        plt.clf()

        plt.plot(np.abs(np.fft.fftshift(np.fft.fft(np.concatenate((a_load, a_load))))), 'ro')
        plt.savefig(path + "_fft.png")
        plt.clf()

    return path

def gen_ramps(path = "./input.dat", n_periods=128, pause = 64, amplitudes = [1], predist = None, par = None, debug = False):
    period = 128
    l_pause = period * pause
    l_sig = period * n_periods
    length = l_pause + l_sig

    t = np.arange(0, l_sig)
    sig = np.zeros(length * len(amplitudes), dtype=np.complex64)
    for i, amplitude in enumerate(amplitudes):
        sig[length * i + l_pause : length * (i + 1)] = complex(amplitude) * np.exp(t * 2j * np.pi * 1./period)

    if predist is None:
        res = sig
    else:
        res = predist(sig, par)

    res = res.astype(np.complex64)
    res.tofile(path)

    a_load = np.fromfile(path, dtype=np.complex64)
    assert(np.isclose(a_load, res).all()), "Inconsistent stored file"

    if debug == True:
        plt.plot(np.abs(np.concatenate((a_load, a_load))))
        plt.savefig(path + ".png")
        plt.clf()

        plt.plot(np.abs(np.fft.fftshift(np.fft.fft(np.concatenate((a_load, a_load))))), 'ro')
        plt.savefig(path + "_fft.png")
        plt.clf()

    return path
