"""
This is a wrapper for gnu radio generated python script

When heavy computations is done in the same thread as the sending and
receiving it gets disturbed. This server wraps the gnu radio script in order to
run the sending and receiving in a separate process. It gives a tcp interface
to control the parameter of the script during runtime.
"""

import time
import numpy as np
import src.ReceiveDictTcp as rdt

from grc.parallel_measurement import parallel_measurement
top = parallel_measurement()

top.start()

receiver = rdt.ReceiveDictTcp('127.0.0.1', 1112)
receiver.start()

top.dpd_memless_poly_0.set_a1(1)
top.dpd_memless_poly_0.set_a2(0.0)
top.dpd_memless_poly_0.set_a3(0.0)
top.dpd_memless_poly_0.set_a4(0.0)
top.dpd_memless_poly_0.set_a5(0.0)
top.dpd_memless_poly_0.set_a6(0.0)
top.dpd_memless_poly_0.set_a7(0.0)
top.dpd_memless_poly_0.set_a8(0.0)

while True:
    d = receiver.queue.get()
    time.sleep(0.01)

    print(d)
    k = d.keys()[0]
    if k == "a1":
        print(d)
        top.dpd_memless_poly_0.set_a1(d[k])
    if k == "a2":
        top.dpd_memless_poly_0.set_a2(d[k])
    if k == "a3":
        top.dpd_memless_poly_0.set_a3(d[k])
    if k == "a4":
        top.dpd_memless_poly_0.set_a4(d[k])
    if k == "a5":
        top.dpd_memless_poly_0.set_a5(d[k])
    if k == "a6":
        top.dpd_memless_poly_0.set_a6(d[k])
    if k == "a7":
        top.dpd_memless_poly_0.set_a7(d[k])
    if k == "a8":
        top.dpd_memless_poly_0.set_a8(d[k])
    if k == "txgain":
        top.uhd_usrp_sink_0_0.set_gain(d[k])
    if k == "rxgain":
        top.uhd_usrp_source_0.set_gain(d[k])
    if k == "input_path":
        top.blocks_file_source_0.open(str(d[k]), True)
    if k == "quit":
        break

top.stop()
top.wait()
