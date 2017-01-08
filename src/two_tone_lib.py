import numpy as np
import matplotlib.pyplot as plt

def gen_two_tone(path = "./input.dat", predist = None, par = None, debug = False):
    period1 = 3.875
    period2 = 4
    t_both = 124
    assert(t_both / period1 % 1 == 0)
    assert(t_both / period2 % 1 == 0)

    t = np.arange(0,t_both)
    sin1 = np.sin(t * 2 * np.pi * 1./period1)
    sin2 = np.sin(t * 2 * np.pi * 1./period2)
    sig = sin1 + sin2

    if predist is None:
        res = sig
    else:
        res = predist(sig, par)

    res = res / np.max(res)

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

def predist_poly(sig, coefs = []):
    res = sig
    for idx, coef in enumerate(coefs):
        res += sig * np.abs(sig)**(idx+1) * coef #+1 because first correction term is squared
    return res

def analyse_power_spec(spec, debug = False, debug_path="", suffix=""):
    peak_1 = None
    peak_2 = None
    spec_start = 4096
    spec_end = 8192
    first_peak = spec_start + 2048
    second_peak = spec_start + 2114
    delta_freq = 66
    peak_other = []
    if debug: plt.plot(spec[spec_start:spec_end])
    for x in [c * delta_freq + delta_freq//2 for c in range(spec_start//delta_freq)]:
        start = spec_start + x 
        end = spec_start + x + delta_freq
        peak = spec[start:end].max()
        if debug: plt.plot((start-spec_start,end-spec_start), (peak, peak))
        if start < first_peak and end > first_peak:
            peak_1 = peak
            if debug: plt.plot((start-spec_start,end-spec_start), (peak+1, peak+1))
        elif start < second_peak and end > second_peak:
            peak_2 = peak
            if debug: plt.plot((start-spec_start,end-spec_start), (peak+1, peak+1))
        else:
            peak_other.append(peak)
    mean_signal = (peak_1 + peak_2) / 2
    mean_others = np.mean(peak_other)
    score = mean_signal - mean_others
    if debug:
        plt.savefig(debug_path + "/" + str(score) + suffix + ".png")
        plt.clf()
    return score
