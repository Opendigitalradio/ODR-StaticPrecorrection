import matplotlib.pyplot as plt
from scipy import signal


def visualize_sync_signal(s1, s2, delay, offset=0, window_size = 20, over_sampling = 10):
    os = over_sampling
    s1_show = signal.resample(s1, s1.shape[0]*os)
    s2_show = signal.resample(s2, s2.shape[0]*os)
    if(delay < 0):
        print("negativ delay", delay)
        delay_abs = abs(delay)
        s1_idx_start = offset + delay_abs
        s1_idx_end   = offset + window_size + delay_abs
        s2_idx_start = offset
        s2_idx_end   = offset + window_size

        s1_idx_start = int(s1_idx_start * os)
        s1_idx_end   = int(s1_idx_end   * os)
        s2_idx_start = int(s2_idx_start * os)
        s2_idx_end   = int(s2_idx_end   * os)

        plt.plot(1  + s1_show[s1_idx_start:s1_idx_end], label = "s1")
        plt.plot(-1 + s2_show[s2_idx_start:s2_idx_end], label = "s2")
        plt.legend()
        plt.show()
    elif(delay >= 0):
        print("positive delay", delay)
        s1_idx_start = offset
        s1_idx_end   = offset + window_size
        s2_idx_start = offset + delay
        s2_idx_end   = offset + window_size + delay

        s1_idx_start = int(s1_idx_start * os)
        s1_idx_end   = int(s1_idx_end   * os)
        s2_idx_start = int(s2_idx_start * os)
        s2_idx_end   = int(s2_idx_end   * os)

        plt.plot(1  + s1_show[s1_idx_start:s1_idx_end], label = "s1")
        plt.plot(-1 + s2_show[s2_idx_start:s2_idx_end], label = "s2")
        plt.legend()
        plt.show()

def visualize_signals(s1, s2, offset=0, window_size = 20):
    s1_idx_start = offset
    s1_idx_end   = offset + window_size
    s2_idx_start = offset
    s2_idx_end   = offset + window_size

    plt.subplot(211); plt.plot(s1[s1_idx_start:s1_idx_end], label = "s1"), plt.legend()
    plt.subplot(212); plt.plot(s2[s2_idx_start:s2_idx_end], label = "s2"), plt.legend()
    plt.show()
