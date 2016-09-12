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

from Animation import Animation
from CodedFloat import CodedFloat
from Screen import Screen
import sys

filename = sys.argv[1]
with open(filename, "rb") as f:
	data = f.read()

ani = Animation()
for i in range(0, len(data), 9):
	framedata = data[i : i + 9]
	if len(framedata) != 9:
		break

	duration = CodedFloat.decode_value(*CodedFloat.unpack_value(framedata[0])) / 1000
	screen = Screen.deserialize(framedata[1:])
	ani.add(screen, duration)
ani.dump()
