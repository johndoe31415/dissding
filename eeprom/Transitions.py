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

import math
import random
from Screen import Screen
from Animation import Animation

class Transition(object):
	def __init__(self, **kwargs):
		self._frametime = kwargs.get("frametime", 0.1)
		self._total_time = kwargs.get("total_time")

	def _process(self, animation):
		if self._total_time is not None:
			animation.normalize(self._total_time)
		return animation

	def calculate(self, from_screen, to_screen):
		raise Exception(NotImplemented)

class RandomTransition(Transition):
	def calculate(self, from_screen, to_screen):
		from_pts = set(from_screen.to_pixels())
		to_pts = set(to_screen.to_pixels())

		chg_pts = from_pts ^ to_pts
		actions = [ ]
		for point in chg_pts:
			if point in from_pts:
				# Remove
				actions.append((point, False))
			else:
				# Add
				actions.append((point, True))


		random.shuffle(actions)
		animation = Animation()
		animation.add(from_screen, self._frametime)
		screen = from_screen
		for ((x, y), state) in actions:
			screen = screen.set_pixel_to(x, y, state)
			animation.add(screen, self._frametime)
		return self._process(animation)
	
class RearrangeTransition(Transition):
	@staticmethod
	def _path(from_pt, to_pt):
		if from_pt == to_pt:
			yield from_pt
		else:
			(x1, y1) = from_pt
			(x2, y2) = to_pt

			distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
			stepcnt = math.ceil(distance * 0.75)
			stepsizex = (x2 - x1) / stepcnt
			stepsizey = (y2 - y1) / stepcnt
			
			for i in range(stepcnt + 1):
				x = round(x1 + (stepsizex * i))
				y = round(y1 + (stepsizey * i))
				yield (x, y)

	def calculate(self, from_screen, to_screen):
		from_pts = list(from_screen.to_pixels())
		to_pts = list(to_screen.to_pixels())

		if (len(from_pts) == 0) or (len(to_pts) == 0):			
			return RandomTransition(frametime = self._frametime / 2, total_time = self._total_time).calculate(from_screen, to_screen)

		while len(from_pts) < len(to_pts):
			from_pts.append(random.choice(from_pts))
		
		while len(to_pts) < len(from_pts):
			to_pts.append(random.choice(to_pts))

		random.shuffle(to_pts)

		paths = [ ]
		longest = 0
		for (from_pt, to_pt) in zip(from_pts, to_pts):
			path = list(self._path(from_pt, to_pt))
			assert(path[0] == from_pt)
			assert(path[-1] == to_pt)
			longest = max(len(path), longest)
			paths.append(path)

		for path in paths:
			while len(path) < longest:
				path.append(path[-1])
	
		animation = Animation()
		for i in range(longest):
			pixels = set(path[i] for path in paths)
			animation.add(Screen.from_pixels(pixels), self._frametime)

		return self._process(animation)

class FadeViaTransition(Transition):
	def __init__(self, pixel_iterator1, pixel_iterator2, fade_via = False, skip_empty = True, **kwargs):
		Transition.__init__(self, **kwargs)
		self._pixel_iterator1 = pixel_iterator1
		self._pixel_iterator2 = pixel_iterator2
		self._fade_via = fade_via
		self._skip_empty = skip_empty

	def calculate(self, from_screen, to_screen):
		animation = Animation()

		pic = from_screen

		animation.add(pic, self._frametime)
		last_img = pic
		for step in self._pixel_iterator1():
			for (x, y) in step:
				pic = pic.set_pixel_to(x, y, self._fade_via)
			if (last_img != pic) or (not self._skip_empty):
				animation.add(pic, self._frametime)
			last_img = pic
			
		for step in self._pixel_iterator2():
			for (x, y) in step:
				pic = pic.set_pixel_to(x, y, to_screen.get_pixel(x, y))
			if (last_img != pic) or (not self._skip_empty):
				animation.add(pic, self._frametime)
			last_img = pic

		return self._process(animation)

class NoiseTransition(Transition):
	def __init__(self, remove_pixel = 4, **kwargs):
		Transition.__init__(self, **kwargs)
		self._remove_pixel = remove_pixel

	def calculate(self, from_screen, to_screen):
		non_noise_pixel = list((x, y) for x in range(8) for y in range(8))
		noise_pixel = list()

		animation = Animation()

		pic = from_screen
		for i in range(64 // self._remove_pixel):
			for (x, y) in noise_pixel:
				pic = pic.rnd_pixel(x, y)
			animation.add(pic, self._frametime)

			for j in range(self._remove_pixel):
				if len(non_noise_pixel) == 0:
					break
				pixel = random.choice(non_noise_pixel)
				noise_pixel.append(pixel)
				non_noise_pixel.remove(pixel)

		for i in range(64 // self._remove_pixel):
			pic = to_screen
			for (x, y) in noise_pixel:
				pic = pic.rnd_pixel(x, y)
			animation.add(pic, self._frametime)

			for j in range(self._remove_pixel):
				if len(noise_pixel) == 0:
					break
				pixel = random.choice(noise_pixel)
				noise_pixel.remove(pixel)

		return self._process(animation)

