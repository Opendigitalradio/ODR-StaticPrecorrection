
# coding: utf-8

# In[1]:

get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt
import numpy as np
import time
import src.gen_source as gen_source
import src.two_tone_lib as tt

import src.tcp_async as tcp_async
import src.tcp_sync as tcp_sync
import src.dab_util as du
import src.dab_tuning_lib as dt

from live_analyse_py import live_analyse_py


# In[15]:

try:
    __IPYTHON__
    reload(tcp_async)
    reload(tcp_sync)
    reload(gen_source)
    reload(tt)
    reload(du)
    reload(dt)
except:
    pass


# In[3]:

sync = tcp_sync.UhdSyncMsg(packet_size=4*8192,
                           packet_type="".join(["f"]*8192))
async = tcp_async.UhdAsyncMsg()


# In[4]:

top = live_analyse_py()


# In[5]:

top.start()


# In[6]:

top.set_txgain(86)
top.set_rxgain(10)


# In[7]:

top.blocks_file_source_0.open("./../dab_normalized_c64.dat", True)


# In[8]:

sync.has_msg()
async.has_msg()


# In[9]:

tt.gen_two_tone(debug = True)


# In[10]:

msgs = sync.get_msgs(1)
msgs = [np.fft.fftshift(msg) for msg in msgs]


# In[18]:

def measure(param):
    n_avg = 20
    x2, x3, x4, x5, x6, x7, x8 = param
    
    repeat = True
    while repeat:
        #tt.gen_two_tone(debug = True, predist=tt.predist_poly, par=(x2, x3, x4))
        
        top.dpd_memless_poly_0.set_a1(1)
        top.dpd_memless_poly_0.set_a2(x2)
        top.dpd_memless_poly_0.set_a3(x3)
        top.dpd_memless_poly_0.set_a4(x4)
        top.dpd_memless_poly_0.set_a5(x5)
        top.dpd_memless_poly_0.set_a6(x6)
        top.dpd_memless_poly_0.set_a7(x7)
        top.dpd_memless_poly_0.set_a8(x8)
        
        sync.has_msg()
        np.array(sync.get_msgs(0.8))
        msgs = np.array(sync.get_msgs(n_avg))
        scores = np.zeros(n_avg)
        msgs = [np.fft.fftshift(msg) for msg in msgs]
        
        if async.has_msg():
            print ("repeat due to async message")
            continue
            
        a = np.array(msgs)
        mean_msg = a.mean(axis = 0)
        suffix = "x_2_%.3f_x_3_%.3f_x_4_%.3fx_5_%.3fx_6_%.3fx_7_%.3fx_8_%.3f" %                 (x2, x3, x4, x5, x6, x7, x8)
        #sig_to_noise = tt.analyse_power_spec(mean_msg, debug=True, debug_path="/tmp/out", suffix=suffix)
        for i in range(n_avg):
            if i == 0:
                scores[i] = dt.calc_signal_sholder_ratio(msgs[0], sampling_rate=8000000, debug=True, debug_path="/tmp/out", suffix=suffix)
            else:
                scores[i] = dt.calc_signal_sholder_ratio(msgs[0], sampling_rate=8000000)
                
        score = np.mean(scores)
        print(score, x2, x3, x4, x5, x6, x7, x8)
        repeat = False
        
        return score


# In[16]:

def simple_opt(pars, i, d, func):
    par = pars[i]
    test_pars = []
    for x in [-1, 0, 1]:
        new_par = list(pars)
        new_par[i] = par + x * d 
        test_pars.append(new_par)
    res = [func(par_new) for par_new in test_pars]
    sel = np.argmax(res)
    best_par = test_pars[sel]
    return best_par

#pars = [1,1,1]
#i_rand = np.random.randint(0, len(pars))
#pars = simple_opt(pars, i_rand, 0.01, lambda x:np.sum(x))
#pars


# In[ ]:

top.set_txgain(86)
top.set_rxgain(5)

pars = np.zeros(7)

for i in range(10000):
    i_rand = np.random.randint(0, len(pars))
    pars = simple_opt(pars, i_rand, 0.005, measure)


# In[ ]:




# In[ ]:




# In[ ]:




# In[15]:

top.set_txgain(85)

params = []
for x2 in np.linspace(-0.1, 0.1, num = 11):
    for x3 in np.linspace(-0.1, 0.1, num = 11):
        for x4 in np.linspace(-0.1, 0.1, num = 11):
            params.append((x2, x3, x4))
            
t_start = time.time()
for idx, param in enumerate(params):
    measure(param)
    time_per_element = (time.time() - t_start) / (idx + 1)
    print ("Time per Element " + str(time_per_element) +
           ", total: " + str(time_per_element * len(params)),
           ", left: " + str(time_per_element * (len(params) - 1 - idx))
          )


# In[ ]:




# In[31]:

sync.stop()
async.stop()
top.stop()
top.wait()


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



