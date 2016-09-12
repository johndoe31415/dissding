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

import sys
import time
import serial
import enum
import struct
import collections

conn = serial.Serial("/dev/ttyUSB0", baudrate = 9600, timeout = 0.1)

class CmdCode(enum.IntEnum):
	READ_EEPROM = 45
	WRITE_EEPROM = 94
	STOP_PLAYBACK = 147
	RESET = 224

class Frame(object):
	_struct = struct.Struct("< B H 16s H")
	_named_struct = collections.namedtuple("NamedStruct", [ "cmdcode", "location", "data", "cksum" ])
	chunksize = 16

	def __init__(self, cmdcode, location = 0, data = None):
		self._values = {
			"cmdcode": cmdcode,
			"location": location,
			"data": b"",
			"cksum": 0,
		}
		if data is not None:
			self._values["data"] = data

	@property
	def cmdcode(self):
		return self._values["cmdcode"]

	@classmethod
	def _crc_update(cls, crc, value):
		assert(0 <= value <= 255)
		crc = crc ^ (value << 8)
		for i in range(8):
			if crc & 0x8000:
				crc = (crc << 1) ^ 0x1021
			else:
				crc <<= 1
			crc &= 0xffff
		return crc

	@classmethod
	def _calc_checksum(cls, data):
		crc = 0
		for value in data:
			crc = cls._crc_update(crc, value)
		return crc

	def __bytes__(self):
		data = self._struct.pack(*self._named_struct(**self._values))
		self._values["cksum"] = self._calc_checksum(data[:-2])
		data = self._struct.pack(*self._named_struct(**self._values))
		return data

	def tx(self, conn):
		conn.write(bytes(self))
		if self.cmdcode == CmdCode.READ_EEPROM:
			rsp = conn.read(18)
			if (len(rsp) == 18) and (rsp[0] == ord("R")) and (rsp[-1] == ord("r")):
				return rsp[1 : -1]
		elif self.cmdcode == CmdCode.WRITE_EEPROM:
			rsp = conn.read(2)
			return rsp == b"OK"
		elif self.cmdcode == CmdCode.STOP_PLAYBACK:
			rsp = conn.read(2)
			return rsp == b"ST"
		elif self.cmdcode == CmdCode.RESET:
			return True

	def txrpt(self, conn):
		for i in range(3):
			result = self.tx(conn)
			if result is not None:
				return result
			print("Retry...")
			time.sleep(0.2)
		raise Exception("Failed to transmit frame.")

def read_eeprom(conn, size = 8192):
	data = b""
	for i in range((size + (Frame.chunksize - 1)) // Frame.chunksize):
		address = Frame.chunksize * i
		rx1 = Frame(CmdCode.READ_EEPROM, location = address).txrpt(conn)
		rx2 = Frame(CmdCode.READ_EEPROM, location = address).txrpt(conn)
		if rx1 == rx2:
			rx = rx1
		else:
			print("Retry wrong read.")
			rx3 = Frame(CmdCode.READ_EEPROM, location = address).txrpt(conn)
			if rx1 == rx3:
				rx = rx3
			elif rx2 == rx3:
				rx = rx3
			else:
				raise Exception("Failed to read chunk, got three different responses.")

		data += rx
		print("Read: %.1f %%" % (len(data) / size * 100))
	data = data[:size]
	return data

def write_eeprom(conn, data, only_chunks = None):
	for i in range((len(data) + (Frame.chunksize - 1)) // Frame.chunksize):
		if (only_chunks is not None) and (i not in only_chunks):
			continue
		address = Frame.chunksize * i
		chunk = data[address : address + Frame.chunksize]
		frame = Frame(CmdCode.WRITE_EEPROM, location = address, data = chunk)
		rx = frame.txrpt(conn)
		print("Write %d: %.1f %%" % (i, address / len(data) * 100))

def verify_eeprom(conn, good_data):
	readback_data = read_eeprom(conn, len(data))
	bad_chunks = set()
	for i in range((len(data) + (Frame.chunksize - 1)) // Frame.chunksize):
		address = Frame.chunksize * i
		read_chunk = readback_data[address : address + Frame.chunksize]
		good_chunk = good_data[address : address + Frame.chunksize]
		if read_chunk != good_chunk:
			print(read_chunk, good_chunk)
			bad_chunks.add(i)
			print("Chunk differs:", i)
	return bad_chunks

#write_eeprom(conn, b"Das ist ein Test!")

while True:
	if not Frame(CmdCode.STOP_PLAYBACK).txrpt(conn):
		print("Could not stop playback.")
		time.sleep(1)
	else:
		break
print("Device stopped.")
time.sleep(0.5)

if len(sys.argv) == 2:
	with open(sys.argv[1], "rb") as f:
		data = f.read()
	write_eeprom(conn, data)
	bad_chunks = verify_eeprom(conn, data)
	if len(bad_chunks) > 0:
		print("Rewriting bad chunks")
		write_eeprom(conn, data, bad_chunks)
		bad_chunks = verify_eeprom(conn, data)
		if len(bad_chunks) > 0:
			print("Bad chunks still remaining after rewriting, aborting :-(")
else:
	data = read_eeprom(conn, 8192)
	with open("readback.bin", "wb") as f:
		f.write(data)

Frame(CmdCode.RESET).tx(conn)


