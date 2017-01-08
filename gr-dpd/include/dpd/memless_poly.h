/* -*- c++ -*- */
/* 
 * Copyright 2017 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */


#ifndef INCLUDED_DPD_MEMLESS_POLY_H
#define INCLUDED_DPD_MEMLESS_POLY_H

#include <dpd/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace dpd {

    /*!
     * \brief <+description of block+>
     * \ingroup dpd
     *
     */
    class DPD_API memless_poly : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<memless_poly> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of dpd::memless_poly.
       *
       * To avoid accidental use of raw pointers, dpd::memless_poly's
       * constructor is in a private implementation
       * class. dpd::memless_poly::make is the public interface for
       * creating new instances.
       */
      static sptr make(float a1, float a2, float a3, float a4, float a5, float a6, float a7, float a8);

      virtual void set_a1(float sens) = 0;
      virtual void set_a2(float sens) = 0;
      virtual void set_a3(float sens) = 0;
      virtual void set_a4(float sens) = 0;
      virtual void set_a5(float sens) = 0;
      virtual void set_a6(float sens) = 0;
      virtual void set_a7(float sens) = 0;
      virtual void set_a8(float sens) = 0;

    };

  } // namespace dpd
} // namespace gr

#endif /* INCLUDED_DPD_MEMLESS_POLY_H */

