import numpy as np


def complex_exp(freq, samp_rate, periods, phase_deg=0):
    t_max = 1.0 * samp_rate / freq * periods
    t = np.arange(t_max)
    fac = t / samp_rate * freq
    phase = 1j * phase_deg/360*2*np.pi
    ret = np.exp(phase + 1j * 2 * np.pi * fac - 1j * np.pi / 2, dtype=np.complex64)
    return ret
ret = complex_exp(10,40,2)


def gen_file(frequency_0, frequency_1, x1 = 0, x2 = 0, x3 = 0, x4 = 0, samp_rate = 4000000, path = "./np_twotone"):
    tone_0 = complex_exp(frequency_0, samp_rate, samp_rate/frequency_1)
    tone_1 = complex_exp(frequency_1, samp_rate, samp_rate/frequency_0)

    two_tone = (tone_0 + tone_1)
    two_tone = two_tone \
            + np.abs(two_tone)**1 * x1 \
            + np.abs(two_tone)**2 * x2 \
            + np.abs(two_tone)**3 * x3 \
            + np.abs(two_tone)**4 * x4

    two_tone = two_tone / np.max(two_tone) * 0.9

    two_tone.tofile(path)

    a_load = np.fromfile(path, dtype=np.complex64)
    assert(np.isclose(a_load, two_tone).all()), "Inconsistent stored file"

    return path
