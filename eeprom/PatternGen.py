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

import collections
from Animation import Animation
from Screen import Screen

class PatternGen(object):
	@classmethod
	def pixel_order_conv(cls, text):
		order = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-"
		sequence = collections.defaultdict(list)
		text = text.split("\n")
		for (y, line) in enumerate(text):
			line = line.lstrip("\t")
			for (x, char) in enumerate(line):
				pos = order.find(char)
				if pos != -1:
					sequence[pos].append((x, y))
		for key in sorted(sequence.keys()):
			yield sequence[key]

class Worm(PatternGen):
	def __init__(self):
		self._order = list(self.pixel_order_conv("""\
			abcdefgh
			BCDEFGHi
			AVWXYZIj
			zU7890Jk
			yT6-+1Kl
			xS5432Lm
			wRQPONMn
			vutsrqpo
		"""))

	def calculate(self, pixeltime = 0.05):
		anim = Animation()
		screen = Screen(0)
		for ((x, y), ) in self._order:
			screen = screen.set_pixel(x, y)
			anim.add(screen, pixeltime)
		for ((x, y), ) in self._order:
			screen = screen.clr_pixel(x, y)
			anim.add(screen, pixeltime)
		return anim

class Ring(PatternGen):
	def __init__(self):
		self._order = list(self.pixel_order_conv("""\
			aaaaaaaa
			abbbbbba
			abccccba
			abcddcba
			abcddcba
			abccccba
			abbbbbba
			aaaaaaaa
		"""))

	def calculate(self, pixeltime = 0.1):
		anim = Animation()
		screen = Screen(0)

		for i in range(3):
			for pixels in self._order:
				for (x, y) in pixels:
					screen = screen.set_pixel(x, y)
				anim.add(screen, pixeltime)
			for pixels in self._order:
				for (x, y) in pixels:
					screen = screen.clr_pixel(x, y)
				anim.add(screen, pixeltime)
		return anim

