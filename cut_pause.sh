#!/bin/bash

#Cut the first two transmission frames of length 96ms plus 1ms
#Samplerate 8192000 Samples / Second
#64 Bit per complex float
#(96*2 + 1) / 1000 * 8192000 * 64 / 8

dd bs=12648448 skip=1 if=test_dat/out.iq of=out_cut_dpd.iq
