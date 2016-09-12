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
#include <stdbool.h>
#include <avr/wdt.h>
#include "eeprom.h"
#include "max7219.h"
#include "delay.h"

bool do_playback(void);

void playback(void) {
	uint16_t address = 0;
	uint8_t data[9];
	while (do_playback()) {

		wdt_reset();
		i2cAddressPointer(address);
		i2cReadData(data, sizeof(data));
		if (data[0] == 0xff) {
			/* End it */
			return;
		}		

		uint8_t mantissa = (data[0] >> 0) & 0x3f;
		uint8_t exponent = (data[0] >> 6) & 0x3;
		uint16_t millis = (5 + mantissa) * (1 << (3 * exponent));
		for (uint8_t i = 0; i < 8; i++) {
			max7219_setcol(i, data[1 + i]);
		}
		delayMillis(millis);
		address += sizeof(data);
	}
}
