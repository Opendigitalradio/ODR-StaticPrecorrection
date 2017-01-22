#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Live Analyse Dab Poly
# Generated: Mon Jan 16 22:23:29 2017
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
        self.use_lut = use_lut = 1
        self.txgain = txgain = 84
        self.rxgain = rxgain = 10
        self.real = real = 1
        self.imag = imag = 1
        self.freq = freq = 222e6
        self.f_2 = f_2 = 4096000/2 + 66000
        self.f_1 = f_1 = 4096000/2
        self.f2 = f2 = samp_rate / 3.875
        self.f1 = f1 = samp_rate / 4
        self.ampl = ampl = 1

        ##################################################
        # Message Queues
        ##################################################
        uhd_amsg_source_0_msgq_out = blocks_message_burst_source_0_msgq_in = gr.msg_queue(2)

        ##################################################
        # Blocks
        ##################################################
        self._use_lut_range = Range(0, 1, 0.0001, 1, 200)
        self._use_lut_win = RangeWidget(self._use_lut_range, self.set_use_lut, "use_lut", "counter_slider", float)
        self.top_layout.addWidget(self._use_lut_win)
        self._rxgain_range = Range(0, 100, 1, 10, 200)
        self._rxgain_win = RangeWidget(self._rxgain_range, self.set_rxgain, "rxgain", "counter_slider", float)
        self.top_layout.addWidget(self._rxgain_win)
        self._ampl_range = Range(0, 1, 0.0001, 1, 200)
        self._ampl_win = RangeWidget(self._ampl_range, self.set_ampl, "ampl", "counter_slider", float)
        self.top_layout.addWidget(self._ampl_win)
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
        self.uhd_amsg_source_0 = uhd.amsg_source(device_addr="", msgq=uhd_amsg_source_0_msgq_out)
        self._txgain_range = Range(0, 100, 1, 84, 200)
        self._txgain_win = RangeWidget(self._txgain_range, self.set_txgain, "txgain", "counter_slider", float)
        self.top_layout.addWidget(self._txgain_win)
        self._real_range = Range(-1, 1, 0.0001, 1, 200)
        self._real_win = RangeWidget(self._real_range, self.set_real, "real", "counter_slider", float)
        self.top_layout.addWidget(self._real_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
        	1024, #size
        	samp_rate, #samp_rate
        	"", #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(2*2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
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
        self._imag_range = Range(-1, 1, 0.0001, 1, 200)
        self._imag_win = RangeWidget(self._imag_range, self.set_imag, "imag", "counter_slider", float)
        self.top_layout.addWidget(self._imag_win)
        self._f_2_range = Range(1, 8000000, 1, 4096000/2 + 66000, 200)
        self._f_2_win = RangeWidget(self._f_2_range, self.set_f_2, "f_2", "counter_slider", float)
        self.top_layout.addWidget(self._f_2_win)
        self._f_1_range = Range(1, 8000000, 1, 4096000/2, 200)
        self._f_1_win = RangeWidget(self._f_1_range, self.set_f_1, "f_1", "counter_slider", float)
        self.top_layout.addWidget(self._f_1_win)
        self.dpd_clut_0 = dpd.clut()
        self.blocks_null_sink_0_2_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_2 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_vcc((1-use_lut, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((ampl, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((use_lut, ))
        self.blocks_message_burst_source_0 = blocks.message_burst_source(gr.sizeof_char*1, blocks_message_burst_source_0_msgq_in)
        self.blocks_add_xx_1 = blocks.add_vcc(1)
        self.analog_sig_source_x_2 = analog.sig_source_c(samp_rate, analog.GR_TRI_WAVE, 1000, 2, -1 + -1j)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_2, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.blocks_add_xx_1, 0), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.blocks_message_burst_source_0, 0), (self.blocks_null_sink_0_2, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_1, 1))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_multiply_const_vxx_2, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.dpd_clut_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.qtgui_time_sink_x_0, 1))    
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.blocks_add_xx_1, 0))    
        self.connect((self.dpd_clut_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
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
        self.analog_sig_source_x_2.set_sampling_freq(self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_use_lut(self):
        return self.use_lut

    def set_use_lut(self, use_lut):
        self.use_lut = use_lut
        self.blocks_multiply_const_vxx_0.set_k((self.use_lut, ))
        self.blocks_multiply_const_vxx_2.set_k((1-self.use_lut, ))

    def get_txgain(self):
        return self.txgain

    def set_txgain(self, txgain):
        self.txgain = txgain

    def get_rxgain(self):
        return self.rxgain

    def set_rxgain(self, rxgain):
        self.rxgain = rxgain
        self.uhd_usrp_source_0.set_gain(self.rxgain, 0)
        	

    def get_real(self):
        return self.real

    def set_real(self, real):
        self.real = real

    def get_imag(self):
        return self.imag

    def set_imag(self, imag):
        self.imag = imag

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_f_2(self):
        return self.f_2

    def set_f_2(self, f_2):
        self.f_2 = f_2

    def get_f_1(self):
        return self.f_1

    def set_f_1(self, f_1):
        self.f_1 = f_1

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
        self.blocks_multiply_const_vxx_1.set_k((self.ampl, ))


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
