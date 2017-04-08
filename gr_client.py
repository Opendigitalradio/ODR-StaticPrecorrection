"""
This is a client for gr_server.py

It attaches to the tcp sockets of both the gnu radio server and the control
server of gr_server
"""

import time
import numpy as np
import src.tcp_sync as ts
import src.dab_tuning_lib as dt
import pandas as pd
import src.SendDictTcp as sdt

use_fft=True

if use_fft: t1 = ts.UhdSyncMsg(port=47009, packet_size=4*16384, packet_type="f"*16384)
else: t1 = ts.UhdSyncMsg(port=47009, packet_size=4*1, packet_type="f")

sender = sdt.SendDictTcp('127.0.0.1', 1112)

sender.send({"txgain":83})
sender.send({"rxgain":15})
sender.send({"a1":0.8})
sender.send({"a2":0.0})
sender.send({"a3":0.0})
sender.send({"a4":0.0})
sender.send({"a5":0.0})
sender.send({"a6":0.0})
sender.send({"a7":0.0})
sender.send({"a8":0.0})
t1.has_msg()
np.mean(t1.get_msgs(10))

def measure_sholders(verbose = False, raw_data=False, std_max=0.025):
    """
    Measure the soulders of the received fft spectrum. Repeat measurement if
    standard deviation larger than std_max
    """
    for i in range(20):
        try:
            if verbose: print("%d measurement" % i)
            t1.has_msg()
            msgs = t1.get_msgs_fft(200)

            def sig_mean(s): return dt.calc_mean_in_freq_range(np.array(s), 8192000, -700000, 700000)
            def sholder_mean(s): return dt.calc_mean_in_freq_range(np.array(s), 8192000, 900000, 1500000)

            sig = [sig_mean(msg) for msg in msgs]
            sholders = [sholder_mean(msg) for msg in msgs]
            std = np.std(sholders)
            mean = np.mean(sholders)
            std_perc = std/np.abs(mean)
            if verbose == 2:
                print( {"mean":mean, "std":std, "std_perc":std_perc})
            if std_perc > std_max:
                if verbose: print("%.4f std/mean" % (std_perc))
                continue
            else:
                if raw_data: return sholders, sig
                else: return np.mean(sholders), np.mean(sig)
        except Exception as e:
            print (e)
    raise Exception("Variance of measurement to high")

res = []
for i in range(5):
    for txgain in range(80, 89):
        sender.send({"txgain":txgain})

        sender.send({"input_path":"/home/andreas/dab/out_cut.iq"})
        sh, sig = measure_sholders(verbose=0, std_max=100)
        res.append({"txgain":txgain, "shoulder":sh, "sig":sig, "dpd":False})

        sender.send({"input_path":"/home/andreas/dab/out_dpd_cut.iq"})
        sh, sig = measure_sholders(verbose=0, std_max=100)
        res.append({"txgain":txgain, "shoulder":sh, "sig":sig, "dpd":True})

df = pd.DataFrame(res)

df.to_csv("~/dab/doc/dab_mod_sholder.csv")

sender.send({"txgain":20})
sender.send({"rxgain":15})
sender.send({"a1":0.1})
