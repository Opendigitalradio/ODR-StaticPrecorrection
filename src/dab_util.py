import numpy as np
import scipy
import matplotlib.pyplot as plt

c = {
        "bw":1536000
        }

def calc_fft(signal, fft_size = 1024, sampling_rate = 1, plot = False):
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

def lagcorr(x,y,lag=None,verbose=False):
    '''Compute lead-lag correlations between 2 time series.

    <x>,<y>: 1-D time series.
    <lag>: lag option, could take different forms of <lag>:
          if 0 or None, compute ordinary correlation and p-value;
          if positive integer, compute lagged correlation with lag
          upto <lag>;
          if negative integer, compute lead correlation with lead
          upto <-lag>;
          if pass in an list or tuple or array of integers, compute
          lead/lag correlations at different leads/lags.

    Note: when talking about lead/lag, uses <y> as a reference.
    Therefore positive lag means <x> lags <y> by <lag>, computation is
    done by shifting <x> to the left hand side by <lag> with respect to
    <y>.
    Similarly negative lag means <x> leads <y> by <lag>, computation is
    done by shifting <x> to the right hand side by <lag> with respect to
    <y>.

    Return <result>: a (n*2) array, with 1st column the correlation
    coefficients, 2nd column correpsonding p values.

    Currently only works for 1-D arrays.
    '''

    import numpy
    from scipy.stats import pearsonr

    if len(x)!=len(y):
        raise Exception('Input variables of different lengths.')

    #--------Unify types of <lag>-------------
    if numpy.isscalar(lag):
        if abs(lag)>=len(x):
            raise Exception('Maximum lag equal or larger than array.')
        if lag<0:
            lag=-numpy.arange(abs(lag)+1)
        elif lag==0:
            lag=[0,]
        else:
            lag=numpy.arange(lag+1)
    elif lag is None:
        lag=[0,]
    else:
        lag=numpy.asarray(lag)

    #-------Loop over lags---------------------
    result=[]
    if verbose:
        print '\n#<lagcorr>: Computing lagged-correlations at lags:',lag

    for ii in lag:
        if ii<0:
            result.append(pearsonr(x[:ii],y[-ii:]))
        elif ii==0:
            result.append(pearsonr(x,y))
        elif ii>0:
            result.append(pearsonr(x[ii:],y[:-ii]))

    result=numpy.asarray(result)

    return result
