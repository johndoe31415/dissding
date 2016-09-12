#
#	dissding - AVR ATmega8 MAX7219 8x8x dot matrix toy.
#	Copyright (C) 2016-2016 Johannes Bauer
#
#	This file is part of dissding.
#
#	dissding is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	dissding is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with dissding; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <joe@johannes-bauer.com>
#

class CodedFloat(object):
	mantissa_bits = 6
	exponent_bits = 2
	special_values = set([ 255 ])
	assert(mantissa_bits + exponent_bits == 8)

	@classmethod
	def pack_value(cls, mantissa, exponent):
		assert(0 <= mantissa < (1 << cls.mantissa_bits))
		assert(0 <= exponent < (1 << cls.exponent_bits))		
		return mantissa | (exponent << cls.mantissa_bits)

	@classmethod
	def unpack_value(cls, packed):
		mantissa = (packed >> 0) & ((1 << cls.mantissa_bits) - 1)
		exponent = (packed >> cls.mantissa_bits) & ((1 << cls.exponent_bits) - 1)
		return (mantissa, exponent)

	@classmethod
	def encode_value(cls, milliseconds):
		(rpacked, rmillis, rerror) = (None, None, None)
		# This is the most stupid algorithm. But I don't care right now
		for (mantissa, exponent, packed, millis) in cls.enumerate():
			error = abs(milliseconds - millis)			
			if (rpacked is None) or (error < rerror):
				rpacked = packed
				rmillis = millis
				rerror = error
		return (rpacked, rmillis)

	@classmethod
	def decode_value(cls, mantissa, exponent):
		return (5 + mantissa) * (8 ** exponent)
	
	@classmethod
	def enumerate(cls):
		for mantissa in range(2 ** cls.mantissa_bits):
			for exponent in range(2 ** cls.exponent_bits):
				packed = cls.pack_value(mantissa, exponent)
				if packed in cls.special_values:
					continue
				millis = cls.decode_value(mantissa, exponent)
				yield (mantissa, exponent, packed, millis)


if __name__ == "__main__":
	for (mantissa, exponent, packed, millis) in CodedFloat.enumerate():
		print("%5d m=%-3d e=%-3d value=%-3d" % (millis, mantissa, exponent, packed))
	#print(CodedFloat.encode_value(77))
