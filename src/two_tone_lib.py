import numpy as np
import matplotlib.pyplot as plt

def gen_two_tone(path = "./input.dat", predist = None, par = None, debug = False):
    period1 = 3.875
    period2 = 4
    t_both = 124 * 10
    assert(t_both / period1 % 1 == 0)
    assert(t_both / period2 % 1 == 0)

    t = np.arange(0,t_both)
    sin1 = np.exp(t * 2j * np.pi * 1./period1)
    sin2 = np.exp(t * 2j * np.pi * 1./period2)
    #sin1 = np.cos(t * np.pi * 1./period1)
    #sin2 = np.cos(t * np.pi * 1./period2)
    sig = sin1 + sin2

    if predist is None:
        res = sig
    else:
        res = predist(sig, par)

    res = res / np.max(res) * 0.99

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

def analyse_power_spec(spec, threshold=40, debug = False, debug_path="", suffix=""):
    peak_1 = None
    peak_2 = None
    delta_freq = 66
    first_peak = 4096 + 2048
    second_peak = 4096 + 2114
    spec_start = first_peak - delta_freq * 10
    spec_end = second_peak + delta_freq * 10
    peak_other = []
    if debug: plt.plot(spec)
    #find peaks
    for x in [c * delta_freq + delta_freq//2 for c in range((spec_end - spec_start)//delta_freq)]:
        start = spec_start + x
        end = spec_start + x + delta_freq
        peak = spec[start:end].max()
        if start < first_peak and end > first_peak:
            peak_1 = (start, end, peak)
        elif start < second_peak and end > second_peak:
            peak_2 = (start, end, peak)
        else:
            peak_other.append((start, end, peak))
    mean_signal = (peak_1[2] + peak_2[2]) / 2
    #peak_other = [[s,e,p] for s, e, p in peak_other if mean_signal - p < threshold]
    meas = [mean_signal - p for s, e, p in peak_other]
    score = np.min(meas)
    if debug:
        plt.plot((peak_1[0],peak_1[1]), (peak_1[2], peak_1[2]), color='g', linewidth=2)
        plt.plot((peak_2[0],peak_2[1]), (peak_2[2], peak_2[2]), color='g', linewidth=2)
        for start, end, peak in peak_other:
            plt.plot((start, end), (peak, peak), color='r', linewidth=2)
        plt.savefig(debug_path + "/" + str(score) + suffix + ".png")
        plt.clf()
    return score
