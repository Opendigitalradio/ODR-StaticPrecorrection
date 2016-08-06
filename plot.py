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

pp.subplot(311)
pp.plot(measurements[..., 1])
pp.subplot(312)
pp.plot(measurements[..., 2])
pp.subplot(313)
pp.plot(measurements[..., 3])

pp.show()


