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
import time
import socket
import struct
import threading
from Queue import Queue

# TCP ports used to communicate between the flowgraph and the python script
# The flowgraph interleaves 3 float streams :
#  generator magnitude
#  phase difference
#  feedback magnitude
TCP_PORT = 47009

class amplitude_ramp(gr.top_block):
    def __init__(self, txgain):
        gr.top_block.__init__(self, "Amplitude Ramp")

        self.txgain = txgain
        self.source_ampl = 0.1
        self.samp_rate = 4e6
        self.rxgain = 0
        self.freq = 222e6
        self.decim = 4000

        # Two-tone signal generator at 1kHz and 2kHz
        self.analog_sig_source_x_0 = analog.sig_source_c(
                self.samp_rate, analog.GR_COS_WAVE, 1000, self.source_ampl, 0)
        self.analog_sig_source_x_1 = analog.sig_source_c(
                self.samp_rate, analog.GR_COS_WAVE, 2000, self.source_ampl, 0)
        self.blocks_add_xx_0 = blocks.add_vcc(1)

        # Connects to both USRP output and mag/phase converter

        self.uhd_usrp_sink_0 = uhd.usrp_sink(
                "",
                uhd.stream_args(
                    cpu_format="fc32",
                    channels=range(1),
                    ),
                )
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_sink_0.set_gain(self.txgain, 0)

        self.blocks_complex_to_magphase_0 = blocks.complex_to_magphase(1)


        # mag goes to TCP interleaved, phase goes to subtractor. There is
        # no substraction block, so it is done with multiply by -1 and add

        # Feedback from the USRP, goes to the subtractor after mag/phase
        self.blocks_complex_to_magphase_1 = blocks.complex_to_magphase(1)
        self.uhd_usrp_source_0 = uhd.usrp_source(
                "",
                uhd.stream_args(
                    cpu_format="fc32",
                    channels=range(1),
                    ),
                )
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_0.set_gain(self.rxgain, 0)

        self.blocks_invert_signal = blocks.multiply_const_vff((-1, ))
        self.blocks_phase_adder = blocks.add_vff(1)

        # The interleaved takes gen mag, phase diff and feedback mag
        # signals and puts them together. We need to decimate before we interleave
        self.blocks_moving_average_gen = blocks.moving_average_ff(self.decim, 1, 4000)
        self.fir_filter_gen = filter.fir_filter_fff(self.decim, ([1]))
        self.fir_filter_gen.declare_sample_delay(0)

        self.blocks_moving_average_phase = blocks.moving_average_ff(self.decim, 1, 4000)
        self.fir_filter_phase = filter.fir_filter_fff(self.decim, ([1]))
        self.fir_filter_phase.declare_sample_delay(0)

        self.blocks_moving_average_feedback = blocks.moving_average_ff(self.decim, 1, 4000)
        self.fir_filter_feedback = filter.fir_filter_fff(self.decim, ([1]))
        self.fir_filter_feedback.declare_sample_delay(0)

        self.blocks_interleave = blocks.interleave(gr.sizeof_float*1, 1)

        self.blks2_tcp_sink_0 = grc_blks2.tcp_sink(
                itemsize=gr.sizeof_float*1,
                addr="127.0.0.1",
                port=TCP_PORT,
                server=True,
                )

        # Connect outgoing
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_complex_to_magphase_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.uhd_usrp_sink_0, 0))

        self.connect((self.blocks_complex_to_magphase_0, 0),
                (self.blocks_moving_average_gen, 0))
        self.connect((self.blocks_moving_average_gen, 0),
                (self.fir_filter_gen, 0))
        self.connect((self.fir_filter_gen, 0), (self.blocks_interleave, 0))

        self.connect((self.blocks_complex_to_magphase_0, 1),
                (self.blocks_invert_signal, 0))
        self.connect((self.blocks_invert_signal, 0), (self.blocks_phase_adder, 1))

        # Connect feedback
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_complex_to_magphase_1, 0))
        self.connect((self.blocks_complex_to_magphase_1, 1), (self.blocks_phase_adder, 0))
        self.connect((self.blocks_phase_adder, 0), (self.blocks_moving_average_phase, 0))
        self.connect((self.blocks_moving_average_phase, 0), (self.fir_filter_phase, 0))
        self.connect((self.fir_filter_phase, 0), (self.blocks_interleave, 1))

        self.connect((self.blocks_complex_to_magphase_1, 0),
                (self.blocks_moving_average_feedback, 0))
        self.connect((self.blocks_moving_average_feedback, 0),
                (self.fir_filter_feedback, 0))
        self.connect((self.fir_filter_feedback, 0),
                (self.blocks_interleave, 2))

        # connect interleaver output to TCP socket
        self.connect((self.blocks_interleave, 0), (self.blks2_tcp_sink_0, 0))


    def get_txgain(self):
        return self.txgain

    def set_txgain(self, txgain):
        self.txgain = txgain
        self.uhd_usrp_sink_0.set_gain(self.txgain, 0)

    def get_source_ampl(self):
        return self.source_ampl

    def set_source_ampl(self, source_ampl):
        print("Set amplitude to {}".format(source_ampl))
        self.source_ampl = source_ampl
        self.analog_sig_source_x_0.set_amplitude(self.source_ampl)
        self.analog_sig_source_x_1.set_amplitude(self.source_ampl)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)


class RampGenerator(threading.Thread):
    def __init__(self, num_meas):
        threading.Thread.__init__(self)
        self.event_queue_ = Queue()
        self.in_queue_ = Queue()

        self.num_meas = num_meas

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

        amplitudes = [0.1 * x for x in range(10)]
        measurements = []

        for ampl in amplitudes:
            self.set_source_ampl(ampl)

            mag_gen_sum = 0
            phase_diff_sum = 0
            mag_feedback_sum = 0

            for measurement_ix in range(self.num_meas):
                # Receive three floats on the socket
                mag_gen, phase_diff, mag_feedback = struct.unpack(
                        "fff",
                        sock.recv(12))

                mag_gen_sum += mag_gen
                phase_diff_sum += phase_diff
                mag_feedback_sum += mag_feedback

                measurements.append((ampl, mag_gen, mag_feedback, phase_diff))

            mag_gen_avg = mag_gen_sum / self.num_meas
            mag_feedback_avg = mag_feedback_sum / self.num_meas
            phase_diff_avg = phase_diff_sum / self.num_meas

            print("Ampl: {} Out: {:10} In: {:10} phase_diff: {:10}".format(
                ampl, mag_gen_avg, mag_feedback_avg, phase_diff_avg))


        self.event_queue_.put("done")
        self.event_queue_.put(measurements)


parser = argparse.ArgumentParser(description='Two-tone amplitude ramp')

parser.add_argument('--txgain',
        default='10',
        help='txgain for USRP sink',
        required=False)

parser.add_argument('--num-meas',
        default='2000',
        help='number of measurements per amplitude',
        required=False)

cli_args = parser.parse_args()

rampgen = RampGenerator(int(cli_args.num_meas))
rampgen.start()

# this blocks until the flowgraph is up and running, i.e. all sockets
# got a connection
top = amplitude_ramp(float(cli_args.txgain))
top.set_source_ampl(0.1)
top.start()

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
        top.set_source_ampl(event)
        rampgen.confirm_source_ampl_updated()

top.stop()
print("Wait for completion")
top.wait()

print("Done")
