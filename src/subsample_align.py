#!/usr/bin/env python
import numpy as np
from scipy import signal, optimize
import sys
import matplotlib.pyplot as plt
import dab_util as du

def gen_omega(length):
    if (length % 2) == 1:
        raise ValueError("Needs an even length array.")

    halflength = int(length/2)
    factor = 2.0 * np.pi / length

    omega = np.zeros(length, dtype=np.float)
    for i in range(halflength):
        omega[i] = factor * i

    for i in range(halflength, length):
        omega[i] = factor * (i - length)

    return omega;

def subsample_align(sig, ref_sig):
    """Do subsample alignment for sig relative to the reference signal
    ref_sig. The delay between the two must be less than sample

    Returns the aligned signal"""

    n = len(sig)
    if (n % 2) == 1:
        raise ValueError("Needs an even length signal.")
    halflen = int(n/2)

    fft_sig = np.fft.fft(sig)

    omega = gen_omega(n)

    def correlate_for_delay(tau):
        # A subsample offset between two signals corresponds, in the frequency
        # domain, to a linearly increasing phase shift, whose slope
        # corresponds to the delay.
        #
        # Here, we build this phase shift in rotate_vec, and multiply it with
        # our signal.

        rotate_vec = np.exp(1j * tau * omega)
        # zero-frequency is rotate_vec[0], so rotate_vec[N/2] is the
        # bin corresponding to the [-1, 1, -1, 1, ...] time signal, which
        # is both the maximum positive and negative frequency.
        # I don't remember why we handle it differently.
        rotate_vec[halflen] = np.cos(np.pi * tau)

        corr_sig = np.fft.ifft(rotate_vec * fft_sig)

        # TODO why do we only look at the real part? Because it's faster than
        # a complex cross-correlation? Clarify!
        return -np.sum(np.real(corr_sig) * np.real(ref_sig.real))

    optim_result = optimize.minimize_scalar(correlate_for_delay, bounds=(-1,1), method='bounded', options={'disp': True})

    if optim_result.success:
        #print("x:")
        #print(optim_result.x)

        best_tau = optim_result.x

        #print("Found subsample delay = {}".format(best_tau))

        # Prepare rotate_vec = fft_sig with rotated phase
        rotate_vec = np.exp(1j * best_tau * omega)
        rotate_vec[halflen] = np.cos(np.pi * best_tau)
        return np.fft.ifft(rotate_vec * fft_sig)
    else:
        #print("Could not optimize: " + optim_result.message)
        return np.zeros(0, dtype=np.complex64)

if __name__ == "__main__":
    phaseref_filename = "/home/andreas/dab/ODR-StaticPrecorrection/data/samples/sample_orig_0.iq"
    phase_ref = np.fromfile(phaseref_filename, np.complex64)

    delay = 15
    n_up = 32

    print("Generate signal with delay {}/{} = {}".format(delay, n_up, float(delay)/n_up))
    phase_ref_up = signal.resample(phase_ref, phase_ref.shape[0] * n_up)
    phase_ref_up_late = np.append(np.zeros(delay, dtype=np.complex64), phase_ref_up[:-delay])
    phase_ref_late = signal.resample(phase_ref_up_late, phase_ref.shape[0])

    phase_ref_realigned = subsample_align(phase_ref_late, phase_ref)
