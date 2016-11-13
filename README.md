Measure amplifier non-linearity using two-tone signal
=====================================================

HOWTO
-----

  1. Take a USRP B200
  1. Connect its TX to the amplifier you want to measure
  1. Connect the amp to an big enough attenuator in order to reduce power to below 1mW
  1. Connect to the B200 RX

The amplitude ramp script is going to generate a two-tone (1kHz separation)
signal at 222MHz, and record outgoing signal magnitude and phase difference
against the source signal. The measurements are written into a CSV file.

It's your job to ensure you don't overload the B200 input signal power (-15dBm
last time I checked).

Before you can start, use gnuradio-companion to generate dual_tone.py from dual_tone.grc

Then gather some measurements

    ./amplitude_ramp.py --ampl-start 0.15 --ampl-stop 0.5 --ampl-step 0.01 --num-meas 300 --txgain 77

This creates a measurement.csv file you can analyse with

    ./plot.py

That's it for now.
