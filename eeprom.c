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

#include <stdio.h>
#include "i2c.h"
#include "delay.h"

void eeprom_write(uint16_t address, const uint8_t *data, uint8_t length) {
	if (i2cHandshake(0x50, false) != I2C_SUCCESS) goto i2cerr;
	if (i2cTransmitByte((address >> 8) & 0xff) != I2C_SUCCESS) goto i2cerr;
	if (i2cTransmitByte((address >> 0) & 0xff) != I2C_SUCCESS) goto i2cerr;
	for (uint8_t i = 0; i < length; i++) {
		if (i2cTransmitByte(data[i]) != I2C_SUCCESS) goto i2cerr;
	}
i2cerr:
	i2cStop();
	if (length > 0) {
		delayMillis(7);
	}
}

void i2cAddressPointer(uint16_t aAddress) {
	eeprom_write(aAddress, NULL, 0);
}


void i2cReadData(uint8_t *aData, uint8_t aLength) {
	uint8_t errorByte;
	if (i2cHandshake(0x50, true) != I2C_SUCCESS) goto i2cerr2;
	if (i2cReceiveBytes(aData, aLength, &errorByte) != I2C_SUCCESS) goto i2cerr2;
i2cerr2:
	i2cStop();

}

