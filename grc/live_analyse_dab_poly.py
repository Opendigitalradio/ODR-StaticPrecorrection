#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Live Analyse Dab Poly
# Generated: Sun Jan 29 11:34:39 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import dpd
import sip
import sys
import time


class live_analyse_dab_poly(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Live Analyse Dab Poly")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Live Analyse Dab Poly")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "live_analyse_dab_poly")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 8e6
        self.txgain = txgain = 80
        self.rxgain = rxgain = 10
        self.freq = freq = 222e6
        self.f_2 = f_2 = 4096000
        self.f_1 = f_1 = 4096000
        self.f2 = f2 = samp_rate / 3.875
        self.f1 = f1 = samp_rate / 4
        self.ampl = ampl = 0.4
        self.a_8 = a_8 = 0
        self.a_7 = a_7 = 0
        self.a_6 = a_6 = 0
        self.a_5 = a_5 = 0
        self.a_4 = a_4 = 0
        self.a_3 = a_3 = 0
        self.a_2 = a_2 = 0
        self.a_1 = a_1 = 0

        ##################################################
        # Message Queues
        ##################################################
        uhd_amsg_source_0_msgq_out = blocks_message_burst_source_0_msgq_in = gr.msg_queue(2)

        ##################################################
        # Blocks
        ##################################################
        self._txgain_range = Range(0, 100, 1, 80, 200)
        self._txgain_win = RangeWidget(self._txgain_range, self.set_txgain, "txgain", "counter_slider", float)
        self.top_layout.addWidget(self._txgain_win)
        self._rxgain_range = Range(0, 100, 1, 10, 200)
        self._rxgain_win = RangeWidget(self._rxgain_range, self.set_rxgain, "rxgain", "counter_slider", float)
        self.top_layout.addWidget(self._rxgain_win)
        self._f_2_range = Range(1, 8000000, 1, 4096000, 200)
        self._f_2_win = RangeWidget(self._f_2_range, self.set_f_2, "f_2", "counter_slider", float)
        self.top_layout.addWidget(self._f_2_win)
        self._f_1_range = Range(1, 8000000, 1, 4096000, 200)
        self._f_1_win = RangeWidget(self._f_1_range, self.set_f_1, "f_1", "counter_slider", float)
        self.top_layout.addWidget(self._f_1_win)
        self._ampl_range = Range(-1, 1, 0.0001, 0.4, 200)
        self._ampl_win = RangeWidget(self._ampl_range, self.set_ampl, "ampl", "counter_slider", float)
        self.top_layout.addWidget(self._ampl_win)
        self._a_8_range = Range(-1, 1, 0.001, 0, 200)
        self._a_8_win = RangeWidget(self._a_8_range, self.set_a_8, "a_8", "counter_slider", float)
        self.top_layout.addWidget(self._a_8_win)
        self._a_7_range = Range(-1, 1, 0.001, 0, 200)
        self._a_7_win = RangeWidget(self._a_7_range, self.set_a_7, "a_7", "counter_slider", float)
        self.top_layout.addWidget(self._a_7_win)
        self._a_6_range = Range(-1, 1, 0.001, 0, 200)
        self._a_6_win = RangeWidget(self._a_6_range, self.set_a_6, "a_6", "counter_slider", float)
        self.top_layout.addWidget(self._a_6_win)
        self._a_5_range = Range(-1, 1, 0.001, 0, 200)
        self._a_5_win = RangeWidget(self._a_5_range, self.set_a_5, "a_5", "counter_slider", float)
        self.top_layout.addWidget(self._a_5_win)
        self._a_4_range = Range(-1, 1, 0.001, 0, 200)
        self._a_4_win = RangeWidget(self._a_4_range, self.set_a_4, "a_4", "counter_slider", float)
        self.top_layout.addWidget(self._a_4_win)
        self._a_3_range = Range(-1, 1, 0.001, 0, 200)
        self._a_3_win = RangeWidget(self._a_3_range, self.set_a_3, "a_3", "counter_slider", float)
        self.top_layout.addWidget(self._a_3_win)
        self._a_2_range = Range(-1, 1, 0.001, 0, 200)
        self._a_2_win = RangeWidget(self._a_2_range, self.set_a_2, "a_2", "counter_slider", float)
        self.top_layout.addWidget(self._a_2_win)
        self._a_1_range = Range(-1, 1, 0.001, 0, 200)
        self._a_1_win = RangeWidget(self._a_1_range, self.set_a_1, "a_1", "counter_slider", float)
        self.top_layout.addWidget(self._a_1_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_gain(rxgain, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_gain(txgain, 0)
        self.uhd_amsg_source_0 = uhd.amsg_source(device_addr="", msgq=uhd_amsg_source_0_msgq_out)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
        	16000, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.1)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.dpd_memless_poly_0 = dpd.memless_poly(a_1, a_2, a_3, a_4, a_5, a_6, a_7, a_8)
        self.blocks_null_sink_0_2_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_2 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((1, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((ampl, ))
        self.blocks_message_burst_source_0 = blocks.message_burst_source(gr.sizeof_char*1, blocks_message_burst_source_0_msgq_in)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, f_1, 0.45, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, f_2, 0.45, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_message_burst_source_0, 0), (self.blocks_null_sink_0_2, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.dpd_memless_poly_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.dpd_memless_poly_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_null_sink_0_2_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_freq_sink_x_0_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "live_analyse_dab_poly")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_f1(self.samp_rate / 4)
        self.set_f2(self.samp_rate / 3.875)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_txgain(self):
        return self.txgain

    def set_txgain(self, txgain):
        self.txgain = txgain
        self.uhd_usrp_sink_0.set_gain(self.txgain, 0)
        	

    def get_rxgain(self):
        return self.rxgain

    def set_rxgain(self, rxgain):
        self.rxgain = rxgain
        self.uhd_usrp_source_0.set_gain(self.rxgain, 0)
        	

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_f_2(self):
        return self.f_2

    def set_f_2(self, f_2):
        self.f_2 = f_2
        self.analog_sig_source_x_0.set_frequency(self.f_2)

    def get_f_1(self):
        return self.f_1

    def set_f_1(self, f_1):
        self.f_1 = f_1
        self.analog_sig_source_x_1.set_frequency(self.f_1)

    def get_f2(self):
        return self.f2

    def set_f2(self, f2):
        self.f2 = f2

    def get_f1(self):
        return self.f1

    def set_f1(self, f1):
        self.f1 = f1

    def get_ampl(self):
        return self.ampl

    def set_ampl(self, ampl):
        self.ampl = ampl
        self.blocks_multiply_const_vxx_0.set_k((self.ampl, ))

    def get_a_8(self):
        return self.a_8

    def set_a_8(self, a_8):
        self.a_8 = a_8
        self.dpd_memless_poly_0.set_a8(self.a_8)

    def get_a_7(self):
        return self.a_7

    def set_a_7(self, a_7):
        self.a_7 = a_7
        self.dpd_memless_poly_0.set_a7(self.a_7)

    def get_a_6(self):
        return self.a_6

    def set_a_6(self, a_6):
        self.a_6 = a_6
        self.dpd_memless_poly_0.set_a6(self.a_6)

    def get_a_5(self):
        return self.a_5

    def set_a_5(self, a_5):
        self.a_5 = a_5
        self.dpd_memless_poly_0.set_a5(self.a_5)

    def get_a_4(self):
        return self.a_4

    def set_a_4(self, a_4):
        self.a_4 = a_4
        self.dpd_memless_poly_0.set_a4(self.a_4)

    def get_a_3(self):
        return self.a_3

    def set_a_3(self, a_3):
        self.a_3 = a_3
        self.dpd_memless_poly_0.set_a3(self.a_3)

    def get_a_2(self):
        return self.a_2

    def set_a_2(self, a_2):
        self.a_2 = a_2
        self.dpd_memless_poly_0.set_a2(self.a_2)

    def get_a_1(self):
        return self.a_1

    def set_a_1(self, a_1):
        self.a_1 = a_1
        self.dpd_memless_poly_0.set_a1(self.a_1)


def main(top_block_cls=live_analyse_dab_poly, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
