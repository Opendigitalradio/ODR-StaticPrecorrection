#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Do an amplitude ramp and save outgoing samples
# and samples coming back from the USRP. The generated
# signal is a two-tone signal
#
# Compare the outgoing amplitude with the incoming amplitude
# to measure AM/AM compression.
#
# In a second step, compare phase and measre AM/PM compression.
#
# Copyright (C) 2016
# Matthias P. Braendli, matthias.braendli@mpb.li
# http://www.opendigitalradio.org
# Licence: The MIT License, see LICENCE file

import sys
import os

import traceback
from gnuradio import analog
from gnuradio import filter
from gnuradio import blocks
from gnuradio import gr
from gnuradio import uhd
from grc_gnuradio import blks2 as grc_blks2
import argparse
import pickle
import time
import socket
import struct
import threading
import numpy as np
from Queue import Queue
from dual_tone import dual_tone # our flowgraph!
import tcp_async

# TCP ports used to communicate between the flowgraph and the python script
# The flowgraph interleaves 3 float streams :
#  generator magnitude
#  phase difference
#  feedback magnitude
TCP_PORT = 47009 # must be the same as in dual_tone!

def xrange(start, stop, step):
    x = start
    while x < stop:
        yield x
        x += step

class RampGenerator(threading.Thread):
    tcpa = None
    lut_dict = None

    def __init__(self, options, tcpa):
        threading.Thread.__init__(self)
        self.event_queue_ = Queue()
        self.in_queue_ = Queue()

        self.num_meas = int(options.num_meas)
        self.num_meas_to_skip = int(options.num_meas_to_skip)
        self.ampl_start = float(options.ampl_start)
        self.ampl_step = float(options.ampl_step)
        self.ampl_stop = float(options.ampl_stop)

        self.output_file = options.out

        if not options.lut is '':
            self.lut_dict = pickle.load(open(options.lut, "rb"))
            assert(type(self.lut_dict) == dict)
            assert(len(self.lut_dict["ampl"]) > 2)
            assert(len(self.lut_dict["fac"])  > 2)

        self.tcpa = tcpa

    def lut(self, ampl):
        if self.lut_dict is None:
            return 1
        else:
            interp = np.interp(ampl, self.lut_dict["ampl"], self.lut_dict["fac"])
            print("interp " + str(interp))
            print("ampl " + str(ampl))
            return interp

    def set_source_ampl(self, ampl):
        self.event_queue_.put(ampl)
        self.in_queue_.get()

    def wait_on_event(self):
        return self.event_queue_.get()

    def confirm_source_ampl_updated(self):
        self.in_queue_.put(0)

    def run(self):
        try:
            self.run_ex()
        except:
            traceback.print_exc()
        finally:
            self.event_queue_.put("quit")

    def run_ex(self):
        print("Wait before connection")
        time.sleep(3)

        print("Connecting to flowgraph")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", TCP_PORT))
        print("Connected")

        amplitudes = xrange(self.ampl_start, self.ampl_stop, self.ampl_step)
        measurements = []

        for idx, ampl in enumerate(amplitudes):
            print("run ampl " + str(ampl))
            ampl_lut = self.lut(ampl) * ampl
            print("run ampl_lut " + str(ampl_lut))
            measurement_correct = False
            max_iter = 10
            while measurement_correct == False and max_iter > 0:
                max_iter -= 1

                self.set_source_ampl(ampl_lut)

                mag_gen_sum = 0
                phase_diff_sum = 0
                mag_feedback_sum = 0

                for measurement_ignore in range(self.num_meas_to_skip):
                    # Receive and ignore three floats on the socket
                    sock.recv(12)

                measurements_new = []
                for measurement_ix in range(self.num_meas):
                    # Receive three floats on the socket
                    mag_gen, phase_diff, mag_feedback = struct.unpack(
                            "fff",
                            sock.recv(12))

                    phase_diff = phase_diff % 720

                    mag_gen_sum += mag_gen
                    phase_diff_sum += phase_diff
                    mag_feedback_sum += mag_feedback

                    measurements_new.append((ampl, mag_gen, mag_feedback, phase_diff))

                mag_gen_avg = mag_gen_sum / self.num_meas
                mag_feedback_avg = mag_feedback_sum / self.num_meas
                phase_diff_avg = phase_diff_sum / self.num_meas

                #Check asynchronous uhd messages for error
                has_msg = self.tcpa.has_msg()
                if not has_msg:
                    measurements.append([np.mean(meas) for meas in zip(*measurements_new)])
                    measurement_correct = True
                    print("Ampl: {} Out: {:10} In: {:10} phase_diff: {:10}".format(
                        ampl, mag_gen_avg, mag_feedback_avg, phase_diff_avg))
                else:
                    print("Retry measurements")


        name = self.output_file
        pickle.dump(measurements, open(name, "wb"))
        self.tcpa.stop()
        self.event_queue_.put("done")
        self.event_queue_.put(measurements)


parser = argparse.ArgumentParser(description='Two-tone amplitude ramp')

parser.add_argument('--ampl-start',
        default='0.1',
        help='Start amplitude',
        required=False)

parser.add_argument('--ampl-stop',
        default='0.8',
        help='Stop amplitude',
        required=False)

parser.add_argument('--ampl-step',
        default='0.02',
        help='Amplitude steps',
        required=False)

parser.add_argument('--txgain',
        default='10',
        help='txgain for USRP sink',
        required=False)

parser.add_argument('--num-meas',
        default='2000',
        help='number of measurements per amplitude',
        required=False)

parser.add_argument('--num-meas-to-skip',
        default='50',
        help='After each amplitude change, ignore num-meas-to-skip measurements',
        required=False)

parser.add_argument('--decim',
        default='4000',
        help='Interval in samples between when to take the average of the measurements',
        required=False)

parser.add_argument('--lut',
        default='',
        help='Path to look up table file',
        required=False)

parser.add_argument('--out',
        default='measurements.pkl',
        help='Output file for measurements (.pkl)',
        required=False)

cli_args = parser.parse_args()
tcpa = tcp_async.UhdAsyncMsg()

rampgen = RampGenerator(cli_args, tcpa)
rampgen.start()

# this blocks until the flowgraph is up and running, i.e. all sockets
# got a connection
top = dual_tone()

top.set_decim(int(cli_args.decim))
top.set_txgain(float(cli_args.txgain))
top.set_rxgain(0)
top.set_source_ampl(float(cli_args.ampl_start))

time.sleep(.5)

top.start()

try:
    while True:
        event = rampgen.wait_on_event()
        if event == "done":
            measurements = rampgen.wait_on_event()
            fd = open("measurements.csv", "w")
            for m in measurements:
                fd.write(",".join("{}".format(x) for x in m) + "\n")
            fd.close()
            break
        elif event == "quit":
            break
        else:
            print("event")
            print(event)
            top.set_source_ampl(event)
            rampgen.confirm_source_ampl_updated()
finally:
    top.stop()
    print("Wait for completion")
    top.wait()

print("Done")
