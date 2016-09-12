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

import sys
import random

class PixelIterator(object):
	@classmethod
	def lr_tb(cls):
		for y in range(8):
			for x in range(8):
				yield [ (x, y) ]
	
	@classmethod
	def lr(cls):
		for x in range(8):
			yield [ (x, y) for y in range(8) ]
	
	@classmethod
	def rl(cls):
		return reversed(list(cls.lr()))
	
	@classmethod
	def tb(cls):
		for y in range(8):
			yield [ (x, y) for x in range(8) ]
	
	@classmethod
	def bt(cls):
		return reversed(list(cls.tb()))

class Screen(object):
	def __init__(self, content = 0):
		assert(isinstance(content, int) and 0 <= content < (2 ** 64))
		self._content = content
		self._cursor = None

	def __int__(self):
		return self._content

	def rotate90(self):
		new = Screen()
		for x in range(8):
			for y in range(8):
				if self.get_pixel(x, y):	
					(x2, y2) = (y, 7 - x)
					new = new.set_pixel(x2, y2)
		return new
	
	def rotate180(self):
		return self.rotate90().rotate90()

	@classmethod
	def pixel_value(cls, x, y):
		assert(0 <= x < 8)
		assert(0 <= y < 8)
		return (1 << (7 - x)) << (8 * (7 - y))

	def set_cursor(self, x, y):
		self._cursor = (x, y)

	def clr_cursor(self):
		self._cursor = None

	def get_pixel(self, x, y):
		return (self._content & self.pixel_value(x, y)) != 0
	
	def rnd_pixel(self, x, y):
		return self.set_pixel_to(x, y, bool(random.randint(0, 1)))

	def set_pixel_to(self, x, y, value):
		assert(isinstance(value, bool))
		if value:
			content = self._content | self.pixel_value(x, y)
		else:
			content = self._content & ~self.pixel_value(x, y)
		return Screen(content)

	def set_pixel(self, x, y):
		return self.set_pixel_to(x, y, True)
	
	def clr_pixel(self, x, y):
		return self.set_pixel_to(x, y, False)

	def invert_pixel(self, x, y):
		return self.set_pixel_to(x, y, not self.get_pixel(x, y))

	def set_set(self, pixels):
		for (x, y) in pixels:
			self = self.set_pixel(x, y)
		return self
	
	def clr_set(self, pixels):
		for (x, y) in pixels:
			self = self.clr_pixel(x, y)
		return self

	@classmethod
	def set_all_pixels(self):
		return cls(0xffffffffffffffff)

	@classmethod
	def clr_all_pixels(cls):
		return cls(0)

	def invert(self):
		for x in range(8):
			for y in range(8):
				self = self.set_pixel_to(x, y, not self.get_pixel(x, y))
		return self

	@classmethod
	def randomize(cls):
		return cls(random.randint(0, (2 ** 64) - 1))

	def dump(self):
		clrscr = "\x1b[3;J\x1b[H\x1b[2J"
		normal_color_on = "\x1b[31m"
		cursor_color_on = "\x1b[34m"
		color_off = "\x1b[0m"
		dot = "⬤ "
#		halfdot = "◯"
		halfdot = "⭕ "
		sys.stdout.write(clrscr)

		print("┌────────────────┐")
		for y in range(8):
			line = "│"
			for x in range(8):
				is_set = self.get_pixel(x, y)
				is_cursor = ((x, y) == self._cursor)

				if is_set:
					if not is_cursor:
						line += normal_color_on + dot + color_off
					else:
						line += cursor_color_on + dot + color_off
				elif is_cursor:
					line += cursor_color_on + halfdot + color_off
				else:
					line += "  "
			line += "│"
			print(line)
		print("└────────────────┘")

	def to_pixels(self):
		for y in range(8):
			for x in range(8):
				if self.get_pixel(x, y):
					yield (x, y)
	@classmethod
	def from_pixels(cls, pixels):
		value = 0
		for (x, y) in pixels:
			value |= cls.pixel_value(x, y)
		return cls(value)

	def __eq__(self, other):
		return self._content == other._content

	def __neq__(self, other):
		return not (self == other)

	def to_code(self, char, f = None):
		if f is None:
			f = sys.stdout
		print("		\"%s\": parse_char(\"\"\"\\" % (char), file = f)
		for y in range(8):
			line = "			"
			for x in range(8):
				if self.get_pixel(x, y):
					line += "⬤ "
				else:
					line += "  "
			print(line, file = f)
		print("		\"\"\"),", file = f)

	@classmethod
	def deserialize(cls, data):
		assert(len(data) == 8)
		value = sum(value << (8 * byteno) for (byteno, value) in enumerate(reversed(data)))
		return Screen(value).rotate180()

	def __bytes__(self):
		value = int(self.rotate180())
		result = bytes((value >> (8 * i)) & 0xff for i in reversed(range(8)))
		return result

if __name__ == "__main__":
	scr = Screen()
	scr = scr.randomize()
	scr.dump()

