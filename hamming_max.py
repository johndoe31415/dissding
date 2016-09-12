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

import random
import itertools

def hamming_weight(x):
	weight = 0
	while x:
		if x & 1:
			weight += 1
		x >>= 1
	return weight

def hamming_distance(a, b):
	return hamming_weight(a ^ b)

def min_hamming_distance(values):
	mindist = None
	for (a, b) in itertools.combinations(values, 2):
		dist = hamming_distance(a, b)
		if (mindist is None) or (dist < mindist):
			mindist = dist
	return mindist


valuerange = (0, 255)
values = [ random.randint(valuerange[0], valuerange[1]) for i in range(4) ]
cur_distance = min_hamming_distance(values)

while True:
	remove_element = random.randrange(len(values))
	new_values = values[:remove_element] + values[remove_element + 1:]
	new_values.append(random.randint(valuerange[0], valuerange[1]))
	new_distance = min_hamming_distance(new_values)
	if new_distance > cur_distance:
		print("%d %s" % (new_distance, str(sorted(new_values))))
	if new_distance >= cur_distance:
		cur_distance = new_distance
		values = new_values
