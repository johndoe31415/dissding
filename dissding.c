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
#include <util/delay.h>
#include <avr/interrupt.h>
#include <avr/wdt.h>

#include "hal.h"
#include "i2c.h"
#include "rs232.h"
#include "max7219.h"
#include "delay.h"
#include "debug.h"
#include "timer.h"
#include "movie.h"

#define STOP_CONSTANT 0xe94745d0UL

volatile uint32_t playback_var;

bool do_playback(void) {
	return playback_var != STOP_CONSTANT;
}

void stop_playback(void) {
	playback_var = STOP_CONSTANT;
}

int main() {
	wdt_reset();
	wdt_enable(WDTO_2S);
	max7219_init();
	delayMillis(250);
	wdt_reset();
	initHAL();
	max7219_init();
	rs232_init();
	//debug_init();
	timer_init();
	sei();

	wdt_enable(WDTO_2S);
	while (true) {
		if (do_playback()) {
			max7219_init();
			playback();
		}
	}

	return 0;
}
