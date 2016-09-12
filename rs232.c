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
#include <stdint.h>
#include <stdbool.h>
#include <avr/interrupt.h>
#include <avr/io.h>
#include <avr/wdt.h>
#include <util/crc16.h>

#include "rs232.h"
#include "debug.h"
#include "timer.h"
#include "eeprom.h"
#include "assert.h"

#define CMDCODE_READ_EEPROM		45
#define CMDCODE_PGM_EEPROM		94
#define CMDCODE_STOP_PLAYBACK	147
#define CMDCODE_RESET			224

struct msg_t {
	uint8_t cmdcode;
	uint16_t address;
	uint8_t data[16];
	uint16_t cksum;
};

#define MSGBUF_SIZE				sizeof(struct msg_t)
staticassert(MSGBUF_SIZE == 21);

static volatile uint8_t msgbuf[MSGBUF_SIZE];
static volatile uint8_t fill;

static uint16_t crc_update(uint16_t crc, uint8_t value) {
	return _crc_xmodem_update(crc, value);
}

static uint16_t calc_cksum(const struct msg_t *data) {
	uint16_t value = 0;
	for (uint8_t i = 0; i < MSGBUF_SIZE - 2; i++) {
		value = crc_update(value, ((const uint8_t*)data)[i]);
	}
	return value;
}

static bool cksum_correct(const struct msg_t *data) {
	return calc_cksum(data) == data->cksum;
}

void stop_playback(void);

extern volatile uint32_t playback_var;
static void check_message(struct msg_t *data) {
	wdt_reset();
	if (!cksum_correct(data)) {
		rs232_transmit('!');
		return;
	}

	if (data->cmdcode == CMDCODE_READ_EEPROM) {
		uint8_t eepromdata[16];
		i2cAddressPointer(data->address);
		i2cReadData(eepromdata, sizeof(eepromdata));
		
		rs232_transmit('R');
		for (uint8_t i = 0; i < sizeof(eepromdata); i++) {
			rs232_transmit(eepromdata[i]);
		}
		rs232_transmit('r');
	} else if (data->cmdcode == CMDCODE_PGM_EEPROM) {
		eeprom_write(data->address, data->data, 16);
		rs232_transmit('O');
		rs232_transmit('K');
	} else if (data->cmdcode == CMDCODE_STOP_PLAYBACK) {
		/* Halt playback immediately */
		stop_playback();
		rs232_transmit('S');
		rs232_transmit('T');
		/*
		rs232_transmit(((playback_var >> (7 * 4)) & 0xf) + 'a');
		rs232_transmit(((playback_var >> (6 * 4)) & 0xf) + 'a');
		rs232_transmit(((playback_var >> (5 * 4)) & 0xf) + 'a');
		rs232_transmit(((playback_var >> (4 * 4)) & 0xf) + 'a');
		rs232_transmit(((playback_var >> (3 * 4)) & 0xf) + 'a');
		rs232_transmit(((playback_var >> (2 * 4)) & 0xf) + 'a');
		rs232_transmit(((playback_var >> (1 * 4)) & 0xf) + 'a');
		rs232_transmit(((playback_var >> (0 * 4)) & 0xf) + 'a');
*/
	} else if (data->cmdcode == CMDCODE_RESET) {
		/* Let the WDT do the dirty work */
		wdt_enable(WDTO_15MS);
	} else {
		rs232_transmit('?');
	}
}

static void check_msgbuf(void) {
	if (fill == MSGBUF_SIZE) {
		check_message((struct msg_t*)msgbuf);
		fill = 0;
	}
}

void softtimer_ovf_rs232_reset(void) {
	fill = 0;
}

ISR(USART_RXC_vect) {
	uint8_t data = UDR;
	softtimer_clr_rs232_reset();
	if (fill < MSGBUF_SIZE) {
		msgbuf[fill++] = data;
		check_msgbuf();
	} else {
		fill = 0;
	}
}

void rs232_transmit(unsigned char aChar) {
	while (!(UCSRA & _BV(UDRE)));		/* Wait until data register empty */
	UDR = aChar;
}

void rs232_init(void) {
	UBRRL = 25;											/* 9600 Baud @ 4 MHz */
	UCSRB = _BV(RXCIE) | _BV(TXEN) | _BV(RXEN);			/* Enable transmitter and receiver, RXC IRQ */
}

