import numpy as np


def complex_exp(freq, samp_rate, periods, phase_deg=0):
    t_max = 1.0 * samp_rate / freq * periods
    t = np.arange(t_max)
    fac = t / samp_rate * freq
    phase = 1j * phase_deg/360*2*np.pi
    ret = np.exp(phase + 1j * 2 * np.pi * fac - 1j * np.pi / 2, dtype=np.complex128)
    return ret
ret = complex_exp(10,40,2)


def gen_file(frequency_0, frequency_1, coefs = [], samp_rate = 4000000, path = "./np_twotone", count = 1):
    tone_0 = complex_exp(frequency_0, samp_rate, samp_rate/frequency_1 * count)
    tone_1 = complex_exp(frequency_1, samp_rate, samp_rate/frequency_0 * count)

    min_len = min(tone_0.shape[0], tone_1.shape[0])
    two_tone = (tone_0[0:min_len] + tone_1[0:min_len])
    res = two_tone

    for idx, coef in enumerate(coefs):
        res += two_tone * np.abs(two_tone)**(idx+1) * coef #+1 because first correction term is squared

    res = res / np.max(res) * 0.9

    res = res.astype(np.complex64)
    res.tofile(path)

    a_load = np.fromfile(path, dtype=np.complex64)
    assert(np.isclose(a_load, res).all()), "Inconsistent stored file"

    return path

def gen_file_d(frequency_0, frequency_1, x1 = 0, x2 = 0, x3 = 0, x4 = 0, samp_rate = 4000000, path = "./np_twotone", count = 1):
    tone_0 = complex_exp(frequency_0, samp_rate, samp_rate/frequency_1 * count)
    tone_1 = complex_exp(frequency_1, samp_rate, samp_rate/frequency_0 * count)

    min_len = min(tone_0.shape[0], tone_1.shape[0])
    two_tone = (tone_0[0:min_len] + tone_1[0:min_len])

    two_tone_1 = np.gradient(two_tone)
    two_tone_2 = np.gradient(two_tone_1)
    two_tone_3 = np.gradient(two_tone_2)
    two_tone_4 = np.gradient(two_tone_3)

    two_tone = two_tone \
            + two_tone_1 * x1 \
            + two_tone_2 * x2 \
            + two_tone_3 * x3 \
            + two_tone_4 * x4

    two_tone = two_tone / np.max(two_tone) * 0.9

    two_tone = two_tone.astype(np.complex64)
    two_tone.tofile(path)

    a_load = np.fromfile(path, dtype=np.complex64)
    assert(np.isclose(a_load, two_tone).all()), "Inconsistent stored file"

    return path

def gen_file_i(frequency_0, frequency_1, x1 = 0, x2 = 0, x3 = 0, x4 = 0, samp_rate = 4000000, path = "./np_twotone", count = 1):
    if frequency_0 > frequency_1:
        f = frequency_0
        frequency_1 = frequency_0
        frequency_0 = f

    tone_0 = complex_exp(frequency_0, samp_rate, samp_rate/frequency_1 * count)
    tone_1 = complex_exp(frequency_1, samp_rate, samp_rate/frequency_0 * count)

    df = frequency_1 - frequency_0
    tone_0_0 = complex_exp(frequency_0 - df, samp_rate, samp_rate/frequency_1 * count, pahse = x2)
    tone_0_1 = complex_exp(frequency_1 + df, samp_rate, samp_rate/frequency_1 * count, pahse = x2)


    min_len = min(tone_0.shape[0], tone_1.shape[0])
    two_tone = (tone_0[0:min_len] + tone_1[0:min_len])

    two_tone_1 = np.gradient(two_tone)
    two_tone_2 = np.gradient(two_tone_1)
    two_tone_3 = np.gradient(two_tone_2)
    two_tone_4 = np.gradient(two_tone_3)

    two_tone = two_tone \
            + two_tone_1 * x1 \
            + two_tone_2 * x2 \
            + two_tone_3 * x3 \
            + two_tone_4 * x4

    two_tone = two_tone / np.max(two_tone) * 0.9

    two_tone = two_tone.astype(np.complex64)
    two_tone.tofile(path)

    a_load = np.fromfile(path, dtype=np.complex64)
    assert(np.isclose(a_load, two_tone).all()), "Inconsistent stored file"

    return path

def gen_sin(samples, oversampling, phi):
    t = np.arange(samples, dtype=np.float)
    sig = np.sin(((2*np.pi)/oversampling) * t - np.pi*phi/180.)
    return sig

