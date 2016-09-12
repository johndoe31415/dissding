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

#ifndef __EEPROM_H__
#define __EEPROM_H__

#include <stdint.h>

/*************** AUTO GENERATED SECTION FOLLOWS ***************/
void eeprom_write(uint16_t address, const uint8_t *data, uint8_t length);
void i2cAddressPointer(uint16_t aAddress);
void i2cReadData(uint8_t *aData, uint8_t aLength);
/***************  AUTO GENERATED SECTION ENDS   ***************/

#endif
