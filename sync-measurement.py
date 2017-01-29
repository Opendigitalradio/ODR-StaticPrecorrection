
# coding: utf-8

# In[1]:

get_ipython().magic('matplotlib inline')
import numpy as np
import time;
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.colors as mpcol
import src.dab_util as du


# In[2]:

import src.signal_gen as sg
reload(sg)
reload(du)


# In[3]:

path_in  = "./input.dat"
path_out = "./output.dat"
a_max = 0.95
n_steps = 64
amps = np.linspace(0.001, a_max, num = n_steps)
txgains = (50, 55, 60, 65, 70, 75, 81, 82, 83, 84, 85, 86, 87, 88, 89)
rxgains = (50, 40, 40, 25, 25, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20)


# In[4]:

from grc.amam_amap import amam_amap


# In[5]:

top = amam_amap()


# In[6]:

sg.gen_ramps(amplitudes=amps)


# In[7]:

def fftlag(signal_original, signal_rec):
    """
    Efficient way to find lag between two signals
    Args:
        signal_original: The signal that has been sent
        signal_rec: The signal that has been recored
    """
    c = np.flipud(signal.fftconvolve(signal_original,np.flipud(signal_rec)))
    #plt.plot(c)
    return np.argmax(c) - signal_original.shape[0] + 1
    
#pattern = np.array([-2,2,-1,+3,-5,+7])
#delays = [0,1,2,3,4]
#padding = [0]
#padding_fil = [0]
#
#res = []
#for d in delays:
#    for p in padding:
#        for p2 in padding_fil:
#            a = np.concatenate((pattern, np.zeros(p2)))
#            b = np.concatenate((np.zeros(d), pattern, np.zeros(p)))
#            res.append((d,conv(a,b)))
#res = np.array(res)
#plt.plot(zip(*res)[0], zip(*res)[1], 'p')


# In[ ]:




# In[ ]:




# In[8]:

def get_amp_ratio(ampl_1, ampl_2, a_out_abs, a_in_abs):
    idxs = (a_in_abs > ampl_1) & (a_in_abs < ampl_2)
    ratio = a_out_abs[idxs] / a_in_abs[idxs]
    return ratio.mean(), ratio.var()

def get_phase(ampl_1, ampl_2, a_out, a_in):
    idxs = (np.abs(a_in) > ampl_1) & (np.abs(a_in) < ampl_2)
    ratio = np.angle(a_out[idxs], deg=True) - np.angle(a_in[idxs], deg=True)
    return ratio.mean(), ratio.var()


# In[9]:

def extract_measurement(a_in, a_out, db, a_max, n_steps, debug = False):
    a_in  = du.crop_signal(a_in)
    a_out = du.crop_signal(a_out)
    
    if debug:
        plt.plot(np.abs(a_in.real) + 1, color='b');
        plt.plot(np.abs(a_out.real), color='g');
        plt.show()
    
    #l = min(a_out.shape[0], a_in.shape[0])
    #a_out = a_out[0:l]
    #a_in  = a_in[0:l]
    
    #c = du.lagcorr(np.abs(a_out), np.abs(a_in), 120000)[:,0]
    #c = signal.fftconvolve(a_in, a_out) - a_out.shape[0]
    delay = fftlag(np.abs(a_in), np.abs(a_out))
    
    
    #delay = np.argmax(c)
    a_out = a_out[delay - 1:]
    
    l = min(a_out.shape[0], a_in.shape[0])
    a_out = a_out[0:l]
    a_in  = a_in[0:l]
    
    if debug:
        print ("delay = " + str(delay))
        plt.plot(np.abs(a_in), color='g');
        plt.plot(np.abs(a_out) - 0.5, color='y');
        plt.show()
    
    bins = np.linspace(+0.5/n_steps,a_max + 0.5/n_steps,num=n_steps)
    res = []
    a_out_abs = np.abs(a_out)
    a_in_abs = np.abs(a_in)
    for ampl_1, ampl_2 in zip(bins, bins[1:]):
        res.append(get_amp_ratio(ampl_1, ampl_2, a_out_abs, a_in_abs))
    del a_out_abs
    del a_in_abs
    mean_amp, var_amp = zip(*res)
    
    res = []
    for ampl_1, ampl_2 in zip(bins, bins[1:]):
        res.append(get_phase(ampl_1, ampl_2, a_out, a_in))
    mean_phase, var_phase = zip(*res)
    return mean_amp, var_amp, mean_phase, var_phase, db


# In[ ]:




# In[10]:

res = []

for txgain, rxgain in zip(txgains, rxgains):
    print (txgain, rxgain)
    res_tmp = None
    for i in range(10):
        top.uhd_usrp_sink_0_0.set_gain(txgain)
        top.uhd_usrp_source_0.set_gain(rxgain)
        
        top.file_sink_out.close()
        top.blocks_file_source_0.close()
        
        top.file_sink_out.open(path_out)
        top.blocks_file_source_0.open(path_in, False)
        top.start()
        
        time.sleep(1)
        
        top.stop()
        top.wait()
        
        a_in  = np.fromfile(path_in, dtype=np.complex64)
        a_out = np.fromfile(path_out, dtype=np.complex64)
        res_tmp = extract_measurement(a_in, a_out, txgain, a_max, n_steps, debug=True)
        
        def is_finite(r): return np.all([np.all(np.isfinite(c)) for c in r])
        def has_small_jumps(mean_amp): return np.max(np.abs(np.diff(mean_amp))) / np.median(np.abs(np.diff(mean_amp))) < 100
        
        if is_finite(res_tmp) and has_small_jumps(res_tmp[0]):
            break
        else:
            print (is_finite(res_tmp), has_small_jumps(res_tmp[0]))
        
    res.append(res_tmp)


# In[ ]:




# In[47]:

fig = plt.figure(figsize=(10,10))
ax1 = plt.subplot(211)

def plot_with_label(x, y, color, label):
    ax1.plot(x, y, color=color, label=txgain)
    
for idx, (txgain, rxgain) in enumerate(zip(*(txgains, rxgains))):
    plot_with_label(
        x = amps[1:], 
        y = 10*np.log(res[idx][0])/np.log(10) - rxgain + 102,
        color = mpcol.hsv_to_rgb((idx * 0.75 / len(txgains), 0.6, 1)),
        label = txgain
    )
ax1.set_ylabel("Gain [dB]")

ax2 = plt.subplot(212)

def plot_with_label(x, y, color, label):
    ax2.plot(x, y, color=color, label=txgain)
    
for idx, (txgain, rxgain) in enumerate(zip(*(txgains, rxgains))):
    plot_with_label(
        x = amps[1:],
        y = res[idx][2],
        color = mpcol.hsv_to_rgb((idx * 0.75 / len(txgains), 0.6, 1)),
        label = txgain
    )

ax2.set_ylabel("Pase [degree]")
ax2.set_xlabel("Amplitude")

#legend
# Shrink current axis by 20%
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax1.legend(loc='center left', bbox_to_anchor=(1.05, -0.3))


plt.show()


# In[ ]:




# In[ ]:




# In[205]:




# In[ ]:




# In[ ]:




# In[ ]:



