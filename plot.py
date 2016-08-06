#!/usr/bin/env python2
#
# Plot the contents of the measurements.csv generated
# by amplitude_ramp.py
#
# Copyright (C) 2016
# Matthias P. Braendli, matthias.braendli@mpb.li
# http://www.opendigitalradio.org
# Licence: The MIT License, see LICENCE file

import numpy as np
import matplotlib.pyplot as pp

measurements = np.loadtxt("measurements.csv", delimiter=",")

mag_gen = measurements[..., 1]
mag_feedback = measurements[..., 2]
phase_diff = measurements[..., 3]

pp.figure()
pp.subplot(311)
pp.plot(mag_gen)
pp.subplot(312)
pp.plot(mag_feedback)
pp.subplot(313)
pp.plot(phase_diff)

pp.figure()
pp.scatter(mag_gen, mag_feedback)

pp.figure()
mag_gen_norm = mag_gen / mag_gen.max()
mag_feedback_norm = mag_feedback / mag_feedback.max()
pp.plot(mag_gen_norm - mag_feedback_norm)

pp.show()


