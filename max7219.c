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

#include "hal.h"
#include "max7219.h"
#include "delay.h"

#define MAX7219_COLUMN_ZERO		0x01
#define MAX7219_DECODE_MODE		0x09
#define MAX7219_INTENSITY		0x0a
#define MAX7219_SCAN_LIMIT		0x0b
#define MAX7219_SHUTDOWN		0x0c
#define MAX7219_DISPLAYTEST		0x0f

/*
7               **  
6                  *
5               **  
4                  *
3               **  
2                  *
1               ** 
0               *  *
     7 6 5 4 3 2 1 0

Picture shows:
	spiSend(MAX7219_COLUMN_ZERO + 0, 0x55);
	spiSend(MAX7219_COLUMN_ZERO + 1, 0xaa);
	spiSend(MAX7219_COLUMN_ZERO + 2, 0xab);
*/

static void spiSendByte(uint8_t aByte) {
	for (int8_t i = 7; i >= 0; i--) {
		MOSI_SetConditional(aByte & (1 << i));
		delay_1us();
		SCK_SetActive();
		delay_1us();
		SCK_SetInactive();
	}
}

void spiSend(uint8_t aAddress, uint8_t aData) {
	CS_SetActive();
	spiSendByte(aAddress);
	spiSendByte(aData);
	CS_SetInactive();
}

void max7219_setcol(uint8_t colno, uint8_t value) {
	spiSend(MAX7219_COLUMN_ZERO + colno, value);
}

void max7219_init(void) {
	for (uint8_t try = 0; try < 3; try++) {
		for (uint8_t i = 0; i < 8; i++) {
			spiSend(MAX7219_COLUMN_ZERO + i, 0);
		}
		spiSend(MAX7219_SHUTDOWN, 1);
		spiSend(MAX7219_DECODE_MODE, 0);
		spiSend(MAX7219_SCAN_LIMIT, 7);
		spiSend(MAX7219_INTENSITY, 3);
		spiSend(MAX7219_DISPLAYTEST, 0);
		delayMillis(20);
	}
}

