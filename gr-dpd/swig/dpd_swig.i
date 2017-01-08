/* -*- c++ -*- */

#define DPD_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "dpd_swig_doc.i"

%{
#include "dpd/memless_poly.h"
%}


%include "dpd/memless_poly.h"
GR_SWIG_BLOCK_MAGIC2(dpd, memless_poly);
