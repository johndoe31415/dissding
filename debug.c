/*
	dissding - AVR ATmega8 MAX7219 8x8x dot matrix toy.
	Copyright (C) 2016-2016 Johannes Bauer

	This file is part of dissding.

	dissding is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; this program is ONLY licensed under
	version 3 of the License, later versions are explicitly excluded.

	dissding is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with dissding; if not, write to the Free Software
	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

	Johannes Bauer <joe@johannes-bauer.com>
*/

#include <stdint.h>
#include "debug.h"
#include "max7219.h"

static volatile uint8_t debugvalue;

void debug_setvalue(uint8_t value) {
	if (value & 1) {
		max7219_setcol(1, 1 | 2 | 4 | 8);
		max7219_setcol(2, 1 | 2 | 4 | 8);
	} else {
		max7219_setcol(1, 1 | 0 | 0 | 8); 
		max7219_setcol(2, 1 | 0 | 0 | 8);
	}
	debugvalue = value;
}

void debug_update(void) {
	max7219_setcol(7, debugvalue);
}

void debug_init(void) {
	max7219_setcol(0, 1 | 2 | 4 | 8);
	max7219_setcol(1, 1 | 0 | 0 | 8) ;
	max7219_setcol(2, 1 | 0 | 0 | 8) ;
	max7219_setcol(3, 1 | 2 | 4 | 8);
}
