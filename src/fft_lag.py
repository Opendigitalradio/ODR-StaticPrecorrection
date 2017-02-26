import numpy as np
from numpy.fft import rfftn, irfftn
from scipy.fftpack import (fft, ifft, ifftshift, fft2, ifft2, fftn,
                                   ifftn, fftfreq)
from scipy._lib._version import NumpyVersion
from scipy import signal

########################################
##### Test functions
########################################
def create_triangular_chirp(f = 0.2, periods = 100):
    #f ... per sample
    t_max = periods / float(f)
    t = np.arange(t_max)
    sig = signal.chirp(t, 0, t_max, f)
    triangle = np.linspace(0, t_max, num = t_max) / t_max
    sig = np.multiply(sig, triangle)
    return sig

def add_delay_and_padding(sig, delay=0, padding=0):
    n_sig = sig.shape[0]
    n_total = n_sig + delay + padding
    ret = np.zeros((n_total), dtype=sig.dtype)
    ret[delay:delay + n_sig] = sig
    return ret

def create_test_signal(f=0.05, periods=100, delay=0, padding=0):
    return add_delay_and_padding(create_triangular_chirp(f=f, periods=periods),
                                 delay=delay, padding=padding)

def visualize_test_signal(f=0.05, periods=100, delay=10, padding=100):
    plt.plot(create_test_signal(f=f, periods=periods, delay=delay, padding=padding))

def down_sample(sig, n_every):
    return sig[::n_every]



_rfft_mt_safe = (NumpyVersion(np.__version__) >= '1.9.0.dev-e24486e')

def _next_regular(target):
    """
    Find the next regular number greater than or equal to target.
    Regular numbers are composites of the prime factors 2, 3, and 5.
    Also known as 5-smooth numbers or Hamming numbers, these are the optimal
    size for inputs to FFTPACK.
    Target must be a positive integer.
    """
    if target <= 6:
        return target

    # Quickly check if it's already a power of 2
    if not (target & (target-1)):
        return target

    match = float('inf')  # Anything found will be smaller
    p5 = 1
    while p5 < target:
        p35 = p5
        while p35 < target:
            # Ceiling integer division, avoiding conversion to float
            # (quotient = ceil(target / p35))
            quotient = -(-target // p35)

            # Quickly find next power of 2 >= quotient
            try:
                p2 = 2**((quotient - 1).bit_length())
            except AttributeError:
                # Fallback for Python <2.7
                p2 = 2**(len(bin(quotient - 1)) - 2)

            N = p2 * p35
            if N == target:
                return N
            elif N < match:
                match = N
            p35 *= 3
            if p35 == target:
                return p35
        if p35 < match:
            match = p35
        p5 *= 5
        if p5 == target:
            return p5
    if p5 < match:
        match = p5
    return match

def fft_lag(s1, s2, n_up = 1, debug=False):
    if debug:
        import matplotlib.pyplot as plt
    s1 = np.flipud(s1) #mult becomes convolution -> filp to get correlation

    sh1 = np.array(s1.shape)
    sh2 = np.array(s2.shape)
    complex_result = (np.issubdtype(s1.dtype, np.complex) or
                      np.issubdtype(s2.dtype, np.complex))
    shape = (sh1 + sh2 - 1)

    fshape = [_next_regular(int(d)) for d in shape]
    fslice = tuple([slice(0, int(sz)) for sz in shape])

    def upsample_fft(s_fft, n_up):
        n = s_fft.shape[0]
        dtype = s_fft.dtype
        ret = None
        if n % 2 == 0:
            ret = np.zeros((n*n_up), dtype=dtype)
            ret[:n/2] = s_fft[0:n/2]
            ret[-n/2:] = s_fft[-n/2:]
        else:
            ret = np.zeros((n*n_up), dtype=dtype)
            ret[:n/2] = s_fft[0:n/2]
            ret[n/2+1] = s_fft[n/2+1] / 2.
            ret[-(n/2+1)] = s_fft[n/2+1] / 2.
            ret[-n/2:] = s_fft[-n/2:]
        ret = ret * n_up
        return ret

    s1_fft = np.fft.fftn(s1, fshape)
    s2_fft = np.fft.fftn(s2, fshape)
    s1_s2_fft = upsample_fft(s1_fft * s2_fft, n_up)
    s1_s2 = np.fft.ifftn(s1_s2_fft)

    delay = np.argmax(s1_s2) / float(n_up) - sh1[0] + 1
    #peak of correlation - size of original signal (robust against padding at the end)

    if debug:
        plt.subplot(411); plt.plot(s1_fft)
        plt.subplot(412); plt.plot(s2_fft)
        plt.subplot(413); plt.plot(s1_s2_fft)
        plt.subplot(414); plt.plot(s1_s2)
        plt.show()
        print(s1_s2.shape, s1_fft.shape, s2_fft.shape, fshape, fslice)


    #return np.argmax(s1_s2)/float(n_up)
    #return np.argmax(s1_s2)/float(n_up) - s2.shape[0] + 1
    return delay

def fft_lag_random_test(n_tests=1000):
    def r():
        return np.random.randint(0, 1000)
    def rand(n):
        return [np.random.randint(0, 1000) for i in range(n)]

    for i in range(n_tests):
        debug = (i == 0)
        d1, d2, p1, p2 = rand(4)
        n_down = 5
        n_up = 32
        sig1 = down_sample(create_test_signal(delay=d1, padding=p1), n_down)
        sig2 = down_sample(create_test_signal(delay=d2, padding=p2), n_down)

        d1, d2, p1, p2 = [x/float(n_down) for x in [d1, d2, p1, p2]]
        delay = d2 - d1
        delay_meas = fft_lag(sig1, sig2, n_up=n_up, debug = debug)
        tol = 1./n_up
        error = abs(delay - delay_meas)
        assert(error < tol)
    print("%d tests within tolerance" % n_tests)


if __name__ == "__main__":
    fft_lag_random_test()
