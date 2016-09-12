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

import time
from CodedFloat import CodedFloat
from Screen import Screen

class Animation(object):
	def __init__(self):
		self._data = [ ]
		self._sleeps = [ ]

	def add(self, screen, duration, combine = True):
		if (len(self._data) > 0) and (screen == self._data[-1]) and combine:
			self._sleeps[-1] += duration
		else:
			self._data.append(screen)
			self._sleeps.append(duration)

	def dump(self):
		for (screen, duration) in zip(self._data, self._sleeps):
			screen.dump()
			time.sleep(duration)

	def normalize(self, total_time):
		screen_time = total_time / len(self._data)
		self._sleeps = [ screen_time for i in range(len(self._data)) ]
		return self

	def __iadd__(self, animation):
		self._data += animation._data
		self._sleeps += animation._sleeps
		return self

	def __add__(self, animation):
		result = Animation()
		result._data = self._data + animation._data
		result._sleeps = self._sleeps + animation._sleeps
		return result

	def pause(self, duration):
		self._data.append(self._data[-1])
		self._sleeps.append(duration)

	def loop(self):
		while True:
			self.dump()

	def reverse(self):
		animation = Animation()
		animation._data = list(reversed(self._data))
		animation._sleeps = list(reversed(self._sleeps))
		return animation
	
	def invert(self):
		animation = Animation()
		animation._data = [ screen.invert() for screen in self._data ]
		animation._sleeps = list(self._sleeps)
		return animation

	def append_inverted(self):
		self._data += [ frame.invert() for frame in self._data ]
		self._sleeps += self._sleeps
		return self

	def __bytes__(self):
		data = bytearray()
		for (screen, duration) in zip(self._data, self._sleeps):
			millis = round(duration * 1000)
			(durationbyte, actual_millis) = CodedFloat.encode_value(millis)
			data += bytes([ durationbyte ]) + bytes(screen)
		data += bytes([ 255 ])
		return bytes(data)

	def make_watchdog_safe(self, max_duration):
		result = Animation()
		for (frame, frame_duration) in zip(self._data, self._sleeps):
			remaining = frame_duration
			while remaining > 0:
				next_duration = remaining
				if next_duration > max_duration:
					next_duration = max_duration
				remaining -= next_duration
				result.add(frame, next_duration, combine = False)
		return result

	@classmethod
	def load_from_file(cls, filename, screentime = 0.1):
		animation = cls()
		with open(filename, "r") as f:
			for line in f:
				value = int(line.rstrip("\r\n"))
				animation.add(Screen(value), screentime)
		return animation

	def __str__(self):
		return "%d images, %.1f secs" % (len(self._data), sum(self._sleeps))

