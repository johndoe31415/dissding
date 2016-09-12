#!/usr/bin/python3
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

import csv
import random
import collections
from Animation import Animation
from Screen import Screen, PixelIterator
from CharDB import CharDB
from Transitions import RandomTransition, RearrangeTransition, FadeViaTransition, NoiseTransition
from PatternGen import Worm, Ring

char_transition_pool = [
	RandomTransition(total_time = 0.3),
	RearrangeTransition(total_time = 0.3),
	FadeViaTransition(pixel_iterator1 = PixelIterator.bt, pixel_iterator2 = PixelIterator.lr_tb, frametime = 0.05),
	FadeViaTransition(pixel_iterator1 = PixelIterator.lr, pixel_iterator2 = PixelIterator.rl, frametime = 0.05),
	NoiseTransition(frametime = 0.02),
]

final_animation_pool = [
	Worm().calculate(0.015),
	Ring().calculate(0.07),
	Animation.load_from_file("animations/cross.anim", 0.1).append_inverted(),
	Animation.load_from_file("animations/downfall.anim", 0.1).append_inverted(),
	Animation.load_from_file("animations/outin.anim", 0.1).append_inverted(),
	Animation.load_from_file("animations/triangle.anim", 0.025).append_inverted(),
	Animation.load_from_file("animations/triangle2.anim", 0.1).append_inverted(),
]

ProdEntry = collections.namedtuple("ProdEntry", [ "serial", "name", "transition_index", "animation_index", "text" ])
production_data = [ ]

with open("production.csv") as f:
	for line in csv.reader(f):
		if len(line) == 4:
			entry = ProdEntry(int(line[0]), line[1], int(line[2]), int(line[3]), text = None)
			production_data.append(entry)

production_data = [
	#ProdEntry(serial = 0, text = " Hello YouTube! ", name = "youtube", transition_index = 1, animation_index = 0),
	ProdEntry(serial = 0, text = " Thanks for watching! ", name = "youtube", transition_index = 2, animation_index = 1),
]

for entry in production_data:
	output_filename = "production_%02d_%s.bin" % (entry.serial, entry.name.lower())

	ani = Animation()
	char_transition = char_transition_pool[entry.transition_index]

	last = None
	if entry.text is None:
		text = " Danke " + entry.name + " "	
	else:
		text = entry.text
	chars = [ CharDB.load_char(c) for c in text ]
#	chars += [ CharDB.load_char(":-)") ]
	for char in chars:
		if last is not None:
			ani += char_transition.calculate(last, char)
		ani.add(char, 0.3)
		last = char
	ani.pause(2)
	ani += final_animation_pool[entry.animation_index]
	ani.pause(1)

	ani = ani.make_watchdog_safe(1.5)
	with open(output_filename, "wb") as f:
		f.write(bytes(ani))

