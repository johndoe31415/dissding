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

import textwrap
from Screen import Screen
	
def parse_char(text):
	text = text.split("\n")
	value = 0
	for (lineindex, line) in enumerate(text):
		line = line.lstrip("\t")
		for charindex in range(0, len(line), 2):
			char = line[charindex]
			if char != "⬤" and (line[charindex] != line[charindex + 1]):
				raise Exception("Inconsistent at line %d col %d" % (lineindex + 1, charindex + 1))
			if char != " ":
				y = lineindex
				x = charindex // 2
				value |= Screen.pixel_value(x, y)
	return Screen(value)

class CharDB(object):
	_CHARS = {
		" ": Screen(0),
		"!": parse_char("""\
			        ⬤       
			        ⬤       
			        ⬤       
			        ⬤       
			                
			                
			        ⬤       
			                
		"""),
		"\"": parse_char("""\
			      ⬤   ⬤     
			      ⬤   ⬤     
			      ⬤   ⬤     
			                
			                
			                
			                
			                
		"""),
		"#": parse_char("""\
			      ⬤   ⬤     
			      ⬤   ⬤     
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			      ⬤   ⬤     
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			      ⬤   ⬤     
			      ⬤   ⬤     
			                
		"""),
		"$": parse_char("""\
			        ⬤       
			      ⬤ ⬤ ⬤ ⬤   
			    ⬤   ⬤       
			      ⬤ ⬤ ⬤     
			        ⬤   ⬤   
			    ⬤ ⬤ ⬤ ⬤     
			        ⬤       
			                
		"""),
		"%": parse_char("""\
			    ⬤ ⬤         
			    ⬤ ⬤     ⬤   
			          ⬤     
			        ⬤       
			      ⬤         
			    ⬤     ⬤ ⬤   
			          ⬤ ⬤   
			                
		"""),
		"&": parse_char("""\
			      ⬤ ⬤       
			    ⬤     ⬤     
			    ⬤   ⬤       
			      ⬤         
			    ⬤   ⬤   ⬤   
			    ⬤     ⬤     
			      ⬤ ⬤   ⬤   
			                
		"""),
		"'": parse_char("""\
			      ⬤ ⬤       
			        ⬤       
			      ⬤         
			                
			                
			                
			                
			                
		"""),
		"(": parse_char("""\
			          ⬤     
			        ⬤       
			      ⬤         
			      ⬤         
			      ⬤         
			        ⬤       
			          ⬤     
			                
		"""),
		")": parse_char("""\
			      ⬤         
			        ⬤       
			          ⬤     
			          ⬤     
			          ⬤     
			        ⬤       
			      ⬤         
			                
		"""),
		"*": parse_char("""\
			                
			        ⬤       
			    ⬤   ⬤   ⬤   
			      ⬤ ⬤ ⬤     
			    ⬤   ⬤   ⬤   
			        ⬤       
			                
			                
		"""),
		"+": parse_char("""\
			                
			        ⬤       
			        ⬤       
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			        ⬤       
			        ⬤       
			                
			                
		"""),
		",": parse_char("""\
			                
			                
			                
			                
			      ⬤ ⬤       
			        ⬤       
			      ⬤         
			                
		"""),
		"-": parse_char("""\
			                
			                
			                
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			                
			                
			                
			                
		"""),
		".": parse_char("""\
			                
			                
			                
			                
			                
			      ⬤ ⬤       
			      ⬤ ⬤       
			                
		"""),
		"/": parse_char("""\
			                
			            ⬤   
			          ⬤     
			        ⬤       
			      ⬤         
			    ⬤           
			                
			                
		"""),
		"0": parse_char("""\
			      ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤     ⬤ ⬤   
			    ⬤   ⬤   ⬤   
			    ⬤ ⬤     ⬤   
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤     
			                
		"""),
		"1": parse_char("""\
			        ⬤       
			      ⬤ ⬤       
			        ⬤       
			        ⬤       
			        ⬤       
			        ⬤       
			      ⬤ ⬤ ⬤     
			                
		"""),
		"2": parse_char("""\
			      ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			            ⬤   
			          ⬤     
			        ⬤       
			      ⬤         
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			                
		"""),
		"3": parse_char("""\
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			          ⬤     
			        ⬤       
			          ⬤     
			            ⬤   
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤     
			                
		"""),
		"4": parse_char("""\
			          ⬤     
			        ⬤ ⬤     
			      ⬤   ⬤     
			    ⬤     ⬤     
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			          ⬤     
			          ⬤     
			                
		"""),
		"5": parse_char("""\
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			    ⬤           
			    ⬤           
			    ⬤ ⬤ ⬤ ⬤     
			            ⬤   
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤     
			                
		"""),
		"6": parse_char("""\
			        ⬤ ⬤     
			      ⬤         
			    ⬤           
			    ⬤ ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤     
			                
		"""),
		"7": parse_char("""\
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			            ⬤   
			          ⬤     
			        ⬤       
			      ⬤         
			      ⬤         
			      ⬤         
			                
		"""),
		"8": parse_char("""\
			      ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤     
			                
		"""),
		"9": parse_char("""\
			      ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤ ⬤   
			            ⬤   
			          ⬤     
			      ⬤ ⬤       
			                
		"""),
		":": parse_char("""\
			                
			      ⬤ ⬤       
			      ⬤ ⬤       
			                
			      ⬤ ⬤       
			      ⬤ ⬤       
			                
			                
		"""),
		";": parse_char("""\
			                
			      ⬤ ⬤       
			      ⬤ ⬤       
			                
			      ⬤ ⬤       
			        ⬤       
			      ⬤         
			                
		"""),
		"<": parse_char("""\
			          ⬤     
			        ⬤       
			      ⬤         
			    ⬤           
			      ⬤         
			        ⬤       
			          ⬤     
			                
		"""),
		"=": parse_char("""\
			                
			                
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			                
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			                
			                
			                
		"""),
		">": parse_char("""\
			    ⬤           
			      ⬤         
			        ⬤       
			          ⬤     
			        ⬤       
			      ⬤         
			    ⬤           
			                
		"""),
		"?": parse_char("""\
			      ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			            ⬤   
			          ⬤     
			        ⬤       
			                
			        ⬤       
			                
		"""),
		"@": parse_char("""\
			      ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			            ⬤   
			      ⬤ ⬤   ⬤   
			    ⬤   ⬤   ⬤   
			    ⬤   ⬤   ⬤   
			      ⬤ ⬤ ⬤     
			                
		"""),
		"A": parse_char("""\
			      ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			                
		"""),
		"B": parse_char("""\
			    ⬤ ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤ ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤ ⬤ ⬤ ⬤     
			                
		"""),
		"C": parse_char("""\
			      ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤           
			    ⬤           
			    ⬤           
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤     
			                
		"""),
		"D": parse_char("""\
			    ⬤ ⬤ ⬤       
			    ⬤     ⬤     
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤     ⬤     
			    ⬤ ⬤ ⬤       
			                
		"""),
		"E": parse_char("""\
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			    ⬤           
			    ⬤           
			    ⬤ ⬤ ⬤ ⬤     
			    ⬤           
			    ⬤           
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			                
		"""),
		"F": parse_char("""\
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			    ⬤           
			    ⬤           
			    ⬤ ⬤ ⬤ ⬤     
			    ⬤           
			    ⬤           
			    ⬤           
			                
		"""),
		"G": parse_char("""\
			      ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤           
			    ⬤   ⬤ ⬤ ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤ ⬤   
			                
		"""),
		"H": parse_char("""\
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			                
		"""),
		"I": parse_char("""\
			      ⬤ ⬤ ⬤     
			        ⬤       
			        ⬤       
			        ⬤       
			        ⬤       
			        ⬤       
			      ⬤ ⬤ ⬤     
			                
		"""),
		"J": parse_char("""\
			        ⬤ ⬤ ⬤   
			          ⬤     
			          ⬤     
			          ⬤     
			          ⬤     
			    ⬤     ⬤     
			      ⬤ ⬤       
			                
		"""),
		"K": parse_char("""\
			    ⬤       ⬤   
			    ⬤     ⬤     
			    ⬤   ⬤       
			    ⬤ ⬤         
			    ⬤   ⬤       
			    ⬤     ⬤     
			    ⬤       ⬤   
			                
		"""),
		"L": parse_char("""\
			    ⬤           
			    ⬤           
			    ⬤           
			    ⬤           
			    ⬤           
			    ⬤           
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			                
		"""),
		"M": parse_char("""\
			    ⬤       ⬤   
			    ⬤ ⬤   ⬤ ⬤   
			    ⬤   ⬤   ⬤   
			    ⬤   ⬤   ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			                
		"""),
		"N": parse_char("""\
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤ ⬤     ⬤   
			    ⬤   ⬤   ⬤   
			    ⬤     ⬤ ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			                
		"""),
		"O": parse_char("""\
			      ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤     
			                
		"""),
		"P": parse_char("""\
			    ⬤ ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤ ⬤ ⬤ ⬤     
			    ⬤           
			    ⬤           
			    ⬤           
			                
		"""),
		"Q": parse_char("""\
			      ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤   ⬤   ⬤   
			    ⬤     ⬤     
			      ⬤ ⬤   ⬤   
			                
		"""),
		"R": parse_char("""\
			    ⬤ ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤ ⬤ ⬤ ⬤     
			    ⬤   ⬤       
			    ⬤     ⬤     
			    ⬤       ⬤   
			                
		"""),
		"S": parse_char("""\
			      ⬤ ⬤ ⬤ ⬤   
			    ⬤           
			    ⬤           
			      ⬤ ⬤ ⬤     
			            ⬤   
			            ⬤   
			    ⬤ ⬤ ⬤ ⬤     
			                
		"""),
		"T": parse_char("""\
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			        ⬤       
			        ⬤       
			        ⬤       
			        ⬤       
			        ⬤       
			        ⬤       
			                
		"""),
		"U": parse_char("""\
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤     
			                
		"""),
		"V": parse_char("""\
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			      ⬤   ⬤     
			        ⬤       
			                
		"""),
		"W": parse_char("""\
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤   ⬤   ⬤   
			    ⬤   ⬤   ⬤   
			    ⬤   ⬤   ⬤   
			      ⬤   ⬤     
			                
		"""),
		"X": parse_char("""\
			    ⬤       ⬤   
			    ⬤       ⬤   
			      ⬤   ⬤     
			        ⬤       
			      ⬤   ⬤     
			    ⬤       ⬤   
			    ⬤       ⬤   
			                
		"""),
		"Y": parse_char("""\
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			      ⬤   ⬤     
			        ⬤       
			        ⬤       
			        ⬤       
			                
		"""),
		"Z": parse_char("""\
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			            ⬤   
			          ⬤     
			        ⬤       
			      ⬤         
			    ⬤           
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			                
		"""),
		"[": parse_char("""\
			      ⬤ ⬤ ⬤     
			      ⬤         
			      ⬤         
			      ⬤         
			      ⬤         
			      ⬤         
			      ⬤ ⬤ ⬤     
			                
		"""),
		"yen": parse_char("""\
			    ⬤       ⬤   
			      ⬤   ⬤     
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			        ⬤       
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			        ⬤       
			        ⬤       
			                
		"""),
		"]": parse_char("""\
			      ⬤ ⬤ ⬤     
			          ⬤     
			          ⬤     
			          ⬤     
			          ⬤     
			          ⬤     
			      ⬤ ⬤ ⬤     
			                
		"""),
		"^": parse_char("""\
			        ⬤       
			      ⬤   ⬤     
			    ⬤       ⬤   
			                
			                
			                
			                
			                
		"""),
		"_": parse_char("""\
			                
			                
			                
			                
			                
			                
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			                
		"""),
		"`": parse_char("""\
			      ⬤         
			        ⬤       
			          ⬤     
			                
			                
			                
			                
			                
		"""),
		"a": parse_char("""\
			                
			                
			      ⬤ ⬤ ⬤     
			            ⬤   
			      ⬤ ⬤ ⬤ ⬤   
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤ ⬤   
			                
		"""),
		"b": parse_char("""\
			    ⬤           
			    ⬤           
			    ⬤   ⬤ ⬤     
			    ⬤ ⬤     ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤ ⬤ ⬤ ⬤     
			                
		"""),
		"c": parse_char("""\
			                
			                
			      ⬤ ⬤ ⬤     
			    ⬤           
			    ⬤           
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤     
			                
		"""),
		"d": parse_char("""\
			            ⬤   
			            ⬤   
			      ⬤ ⬤   ⬤   
			    ⬤     ⬤ ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤ ⬤   
			                
		"""),
		"e": parse_char("""\
			                
			                
			      ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			    ⬤           
			      ⬤ ⬤ ⬤     
			                
		"""),
		"f": parse_char("""\
			        ⬤ ⬤     
			      ⬤     ⬤   
			      ⬤         
			    ⬤ ⬤ ⬤       
			      ⬤         
			      ⬤         
			      ⬤         
			                
		"""),
		"g": parse_char("""\
			                
			                
			      ⬤ ⬤ ⬤ ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤ ⬤   
			            ⬤   
			      ⬤ ⬤ ⬤     
		"""),
		"h": parse_char("""\
			    ⬤           
			    ⬤           
			    ⬤   ⬤ ⬤     
			    ⬤ ⬤     ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			                
		"""),
		"i": parse_char("""\
			        ⬤       
			                
			      ⬤ ⬤       
			        ⬤       
			        ⬤       
			        ⬤       
			      ⬤ ⬤ ⬤     
			                
		"""),
		"j": parse_char("""\
			          ⬤     
			                
			        ⬤ ⬤     
			          ⬤     
			          ⬤     
			    ⬤     ⬤     
			      ⬤ ⬤       
			                
		"""),
		"k": parse_char("""\
			      ⬤         
			      ⬤         
			      ⬤     ⬤   
			      ⬤   ⬤     
			      ⬤ ⬤       
			      ⬤   ⬤     
			      ⬤     ⬤   
			                
		"""),
		"l": parse_char("""\
			      ⬤ ⬤       
			        ⬤       
			        ⬤       
			        ⬤       
			        ⬤       
			        ⬤       
			      ⬤ ⬤ ⬤     
			                
		"""),
		"m": parse_char("""\
			                
			                
			    ⬤ ⬤   ⬤     
			    ⬤   ⬤   ⬤   
			    ⬤   ⬤   ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			                
		"""),
		"n": parse_char("""\
			                
			                
			    ⬤ ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			                
		"""),
		"o": parse_char("""\
			                
			                
			      ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤     
			                
		"""),
		"p": parse_char("""\
			                
			                
			    ⬤ ⬤ ⬤ ⬤     
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤ ⬤ ⬤ ⬤     
			    ⬤           
			    ⬤           
		"""),
		"q": parse_char("""\
			                
			                
			      ⬤ ⬤   ⬤   
			    ⬤     ⬤ ⬤   
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤ ⬤   
			            ⬤   
			            ⬤   
		"""),
		"r": parse_char("""\
			                
			                
			    ⬤   ⬤ ⬤     
			    ⬤ ⬤     ⬤   
			    ⬤           
			    ⬤           
			    ⬤           
			                
		"""),
		"s": parse_char("""\
			                
			                
			      ⬤ ⬤ ⬤     
			    ⬤           
			      ⬤ ⬤ ⬤     
			            ⬤   
			    ⬤ ⬤ ⬤ ⬤     
			                
		"""),
		"t": parse_char("""\
			      ⬤         
			      ⬤         
			    ⬤ ⬤ ⬤       
			      ⬤         
			      ⬤         
			      ⬤     ⬤   
			        ⬤ ⬤     
			                
		"""),
		"u": parse_char("""\
			                
			                
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤     ⬤ ⬤   
			      ⬤ ⬤   ⬤   
			                
		"""),
		"v": parse_char("""\
			                
			                
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			      ⬤   ⬤     
			        ⬤       
			                
		"""),
		"w": parse_char("""\
			                
			                
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤       ⬤   
			    ⬤   ⬤   ⬤   
			      ⬤   ⬤     
			                
		"""),
		"x": parse_char("""\
			                
			                
			    ⬤       ⬤   
			      ⬤   ⬤     
			        ⬤       
			      ⬤   ⬤     
			    ⬤       ⬤   
			                
		"""),
		"y": parse_char("""\
			                
			                
			    ⬤       ⬤   
			    ⬤       ⬤   
			      ⬤ ⬤ ⬤ ⬤   
			            ⬤   
			      ⬤ ⬤ ⬤     
			                
		"""),
		"z": parse_char("""\
			                
			                
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			          ⬤     
			        ⬤       
			      ⬤         
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			                
		"""),
		"{": parse_char("""\
			          ⬤     
			        ⬤       
			        ⬤       
			      ⬤         
			        ⬤       
			        ⬤       
			          ⬤     
			                
		"""),
		"|": parse_char("""\
			        ⬤       
			        ⬤       
			        ⬤       
			        ⬤       
			        ⬤       
			        ⬤       
			        ⬤       
			                
		"""),
		"}": parse_char("""\
			      ⬤         
			        ⬤       
			        ⬤       
			          ⬤     
			        ⬤       
			        ⬤       
			      ⬤         
			                
		"""),
		"->": parse_char("""\
			                
			        ⬤       
			          ⬤     
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			          ⬤     
			        ⬤       
			                
			                
		"""),
		"<-": parse_char("""\
			                
			        ⬤       
			      ⬤         
			    ⬤ ⬤ ⬤ ⬤ ⬤   
			      ⬤         
			        ⬤       
			                
			                
		"""),
		"°": parse_char("""\
			      ⬤ ⬤ ⬤     
			      ⬤   ⬤     
			      ⬤ ⬤ ⬤     
			                
			                
			                
			                
			                
		"""),
		":-)":	Screen(18586215850787388),
	}

	@classmethod
	def load_char(cls, char):
		return cls._CHARS[char]


