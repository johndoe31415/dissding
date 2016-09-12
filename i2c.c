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

#include "hal.h"
#include "i2c.h"
#include "delay.h"

#define I2C_READ_ADDR(x)					(((x & 0x7f) << 1) | 0x01)
#define I2C_WRITE_ADDR(x)					(((x & 0x7f) << 1) | 0x00)

#define SCL_BusLow()						SCL_ModeOutput();
#define SCL_BusHigh()						SCL_ModeInput();
#define SDA_BusLow()						SDA_ModeOutput();
#define SDA_BusHigh()						SDA_ModeInput();

#define SCL_IsLow()							SCL_IsOutput()
#define SCL_IsHigh()						(SCL_IsInput() && SCL_IsActive())
#define SCL_IsFree()						SCL_IsInput()
#define SDA_IsLow()							SDA_IsOutput()
#define SDA_IsHigh()						(SDA_IsInput() && SDA_IsActive())
#define SDA_IsFree()						SDA_IsInput()


static int16_t i2cSoftSCLHigh(void) {
	SCL_BusHigh();
	delay_1us();
	uint16_t timeout = 4000;
	while (--timeout > 0) {
		if (SCL_IsActive()) {
			break;
		}
	}
	return (timeout > 0) ? I2C_SUCCESS : I2C_ERR_SCL_TIMEOUT;
}

/* Precondition: SDA High, SCL High */
static void i2cStart(void) {
	if (SCL_IsLow()) {
		/* Repeated start */
		/* Bring SDA high first */
		SDA_BusHigh();
		delay_1us();

		/* Then SCL high */
		i2cSoftSCLHigh();
		delay_1us();
	}

	/* Normal start */
	SDA_BusLow();
	delay_1us();

	SCL_BusLow();
	delay_1us();
}

/* LOW -> HIGH on SDA while SCL is HIGH */
int16_t i2cStop(void) {
	/* Change SDA to LOW first */
	SDA_BusLow();

	/* Then bring SCL high */
	int16_t result = i2cSoftSCLHigh();
	if (result != I2C_SUCCESS) {
		return result;
	}
	
	/* And then do the LOW -> HIGH transition on SDA */
	SDA_BusHigh();
	delay_1us();

	return I2C_SUCCESS;
}


static int16_t i2cTransmitBit(bool aBit) {
	
	if (aBit) {
		SDA_BusHigh();
	} else {
		SDA_BusLow();
	}

	if (!i2cSoftSCLHigh()) {
		return I2C_ERR_SCL_TIMEOUT;
	}
			
	SCL_BusLow();
	return I2C_SUCCESS;
}

static int16_t i2cReceiveBit(void) {
	/* First free SDA */
	SDA_BusHigh();

	/* Then take SCL high */
	if (!i2cSoftSCLHigh()) {
		return I2C_ERR_SCL_TIMEOUT;
	}
	
	/* And read out SDA */
	int16_t result = SDA_IsActive() ? 1 : 0;
	
	SCL_BusLow();

	return result;
}

int16_t i2cTransmitByte(uint8_t aByte) {
	for (int8_t bit = 7; bit >= 0; bit--) {
		bool bitVal = (aByte & (1 << bit)) != 0;
		int16_t result = i2cTransmitBit(bitVal);
		if (result != I2C_SUCCESS) {
			return result;
		}
	}
	
	int16_t ack = i2cReceiveBit();
	if (ack < 0) {
		return ack;
	} else if (ack == 1) {
		return I2C_ERR_NO_ACK;
	} else {
		return I2C_SUCCESS;
	}
}

static int16_t i2cReceiveByte(bool aSendACK) {
	uint8_t value = 0;

	for (uint8_t bit = 0; bit < 8; bit++) {
		int16_t bitValue = i2cReceiveBit();
		if (bitValue < 0) {
			return bitValue;
		}

		value <<= 1;
		if (bitValue) {
			value |= 0x01;
		}
	}

	/* Send ACK/NACK */
	int16_t sendAckResult = i2cTransmitBit(!aSendACK);
	if (sendAckResult != I2C_SUCCESS) {
		return sendAckResult;
	}
	return value;
}

int16_t i2cReceiveBytes(uint8_t *aDataBuffer, uint8_t aLength, uint8_t *aErrorByte) {
	for (uint8_t i = 0; i < aLength; i++) {
		int16_t result = i2cReceiveByte(i != (aLength - 1));
		if (result < 0) {
			*aErrorByte = i;
			return result;
		}
		aDataBuffer[i] = result;
	}
	return I2C_SUCCESS;
}

int16_t i2cHandshake(uint8_t aAddress, bool aRead) {
	int16_t result;

	i2cStart();
	result = i2cTransmitByte(aRead ? I2C_READ_ADDR(aAddress) : I2C_WRITE_ADDR(aAddress));

	if (result == I2C_ERR_NO_ACK) {
		i2cStop();
	}

	return result;
}

int16_t i2cScanForDevice(uint8_t aAddress) {
	int16_t result;
	
	if ((result = i2cHandshake(aAddress, true)) != I2C_SUCCESS) {
		return result;
	}

	/* If we successfully addressed someone, we need to read at least a
	 * byte and then immediately NACK it */
	int16_t readByte = i2cReceiveByte(false);
	if (readByte < 0) {
		result = readByte;
	}
	i2cStop();
	return result;
}

int16_t i2cReadSingleByte(uint8_t aAddress) {
	uint16_t result;
	i2cStart();
	result = i2cTransmitByte(I2C_READ_ADDR(aAddress));
	if (result != I2C_SUCCESS) {
		i2cStop();
		return result;
	}
	result = i2cReceiveByte(false);
	i2cStop();
	return result;
}

