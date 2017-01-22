/* -*- c++ -*- */

#define DPD_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "dpd_swig_doc.i"

%{
#include "dpd/memless_poly.h"
#include "dpd/lut.h"
#include "dpd/clut.h"
%}


%include "dpd/memless_poly.h"
GR_SWIG_BLOCK_MAGIC2(dpd, memless_poly);
%include "dpd/lut.h"
GR_SWIG_BLOCK_MAGIC2(dpd, lut);
%include "dpd/clut.h"
GR_SWIG_BLOCK_MAGIC2(dpd, clut);
