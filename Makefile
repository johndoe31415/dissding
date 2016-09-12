.PHONY: all doc showheaders showisr clean program sramlayout flashlayout halgen gdb
.SUFFIXES: .c .o .s .S .E .hex .bin .dmp .coff .syms

###################################################################################################

include Makefile.user
include Makefile.build

# {{{ MCU detection

ifeq ($(MCU_UNIT),attiny2313)
MCU_AVRDUDE := t2313
MCU := attiny2313
FLASH_SIZE := $(shell expr 2 \* 1024)
SRAM_SIZE := 128
EEPROM_SIZE := 128
DATASHEET := ATtiny2313_doc2543.pdf
HEADERFILE := iotn2313.h
else
ifeq ($(MCU_UNIT),attiny26)
MCU_AVRDUDE := t26
MCU := attiny26
FLASH_SIZE := $(shell expr 2 \* 1024)
SRAM_SIZE := 128
EEPROM_SIZE := 128
DATASHEET := ATtiny26.pdf
HEADERFILE := iotn26.h
else
ifeq ($(MCU_UNIT),atmega16)
MCU_AVRDUDE := m16
MCU := atmega16
FLASH_SIZE := $(shell expr 16 \* 1024)
SRAM_SIZE := $(shell expr 1 \* 1024)
EEPROM_SIZE := 512
DATASHEET := ATmega16_doc2466.pdf
HEADERFILE := iom16.h
else
ifeq ($(MCU_UNIT),atmega32)
MCU_AVRDUDE := m32
MCU := atmega32
FLASH_SIZE := $(shell expr 32 \* 1024)
SRAM_SIZE := $(shell expr 2 \* 1024)
EEPROM_SIZE := $(shell expr 1 \* 1024)
DATASHEET := ATmega32_doc2503.pdf
HEADERFILE := iom32.h
else
ifeq ($(MCU_UNIT),at90s8515)
MCU_AVRDUDE := AT90S8515
MCU := at90s8515
FLASH_SIZE := $(shell expr 8 \* 1024)
SRAM_SIZE := 512
EEPROM_SIZE := 512
DATASHEET := AT90S8515_doc0841.pdf
HEADERFILE := io8515.h
else
ifeq ($(MCU_UNIT),at90s8535)
MCU_AVRDUDE := AT90S8535
MCU := at90s8535
FLASH_SIZE := $(shell expr 8 \* 1024)
SRAM_SIZE := 512
EEPROM_SIZE := 512
DATASHEET := AT90S8535.pdf
HEADERFILE := io8535.h
else
ifeq ($(MCU_UNIT),at90can128)
MCU_AVRDUDE := c128
MCU := at90can128
FLASH_SIZE := $(shell expr 128 \* 1024)
SRAM_SIZE := $(shell expr 8 \* 1024)
EEPROM_SIZE := $(shell expr 4 \* 1024)
DATASHEET := AT90CAN128.pdf
HEADERFILE := iocanxx.h
else
ifeq ($(MCU_UNIT),atmega128)
MCU_AVRDUDE := m128
MCU := atmega128
FLASH_SIZE := $(shell expr 128 \* 1024)
SRAM_SIZE := $(shell expr 4 \* 1024)
EEPROM_SIZE := $(shell expr 4 \* 1024)
DATASHEET := ATmega128.pdf
HEADERFILE := iom128.h
else
ifeq ($(MCU_UNIT),atmega8)
MCU_AVRDUDE := m8
MCU := atmega8
FLASH_SIZE := $(shell expr 8 \* 1024)
SRAM_SIZE := $(shell expr 1 \* 1024)
EEPROM_SIZE := 512
DATASHEET := ATmega8.pdf
HEADERFILE := iom8.h
else
ifeq ($(MCU_UNIT),atxmega128a1)
MCU_AVRDUDE := x128a1
MCU := atxmega128a1
FLASH_SIZE := $(shell expr 128 \* 1024)
SRAM_SIZE := $(shell expr 8 \* 1024)
EEPROM_SIZE := $(shell expr 2 \* 1024)
DATASHEET := ATxmega128A1.pdf
HEADERFILE := iox128a1.h
else
ifeq ($(MCU_UNIT),atxmega128a1btldr)
MCU_AVRDUDE := x128a1
MCU := atxmega128a1
FLASH_SIZE := $(shell expr 8 \* 1024)
SRAM_SIZE := $(shell expr 8 \* 1024)
EEPROM_SIZE := $(shell expr 2 \* 1024)
DATASHEET := ATxmega128A1.pdf
HEADERFILE := iox128a1.h
else
ifeq ($(MCU_UNIT),attiny13)
MCU_AVRDUDE := t13
MCU := attiny13
FLASH_SIZE := $(shell expr 1 \* 1024)
SRAM_SIZE := 64
EEPROM_SIZE :=64 
DATASHEET := ATtiny13.pdf
HEADERFILE := iot13.h
else
$(error No such unit '$(MCU_UNIT)' which was selected in Makefile.build. Either add the MCU definition to Makefile or change Makefile.build)
endif
endif
endif
endif
endif
endif
endif
endif
endif
endif
endif
endif

# }}}


###################################################################################################

all: $(PROJNAME) $(PROJNAME).S $(PROJNAME)_Flash.hex $(PROJNAME)_EEPROM.hex $(PROJNAME).bin $(PROJNAME).E $(PROJNAME).syms $(PROJNAME).dmp

halgen:
	$(HALGEN) -a avr -o hal.h $(HALINPUT)

doc:
	evince $(DATASHEET_DIRECTORY)$(DATASHEET) &

showheaders:
	@cat $(AVR_LIBC_DIRECTORY)include/avr/$(HEADERFILE)

showisr:
	@cat $(AVR_LIBC_DIRECTORY)include/avr/$(HEADERFILE) | grep '_VECTOR' | grep -E '^#define ' | grep '_vect' | sed 's/_VECTOR(\(.*\))/\1/' | awk '{printf("%2d: %s\n", $$3, $$2);}'

clean:
	rm -f $(PROJNAME) $(PROJNAME).coff $(PROJNAME).syms
	rm -f $(PROJNAME).S $(PROJNAME).E
	rm -f $(PROJNAME)_Flash.hex $(PROJNAME)_EEPROM.hex 
	rm -f $(PROJNAME).bin $(PROJNAME).dmp
	rm -f $(PROJNAME).xml $(PROJNAME).fw
	rm -f $(OBJS)
	rm -f fuse

reset:
	$(AVRDUDE) $(AVRDUDE_OPTS) -p $(MCU_AVRDUDE) -c $(AVRDUDE_PGMR)

program: $(PROJNAME)_Flash.hex
	$(AVRDUDE) $(AVRDUDE_OPTS) -p $(MCU_AVRDUDE) -c $(AVRDUDE_PGMR) -U flash:w:$(PROJNAME)_Flash.hex:i

programall: $(PROJNAME).bin
	$(AVRDUDE) $(AVRDUDE_OPTS) -p $(MCU_AVRDUDE) -c $(AVRDUDE_PGMR) -U flash:w:$(PROJNAME).bin:r -U boot:w:../Bootloader/Bootloader.bin:r

readflash:
	$(AVRDUDE) $(AVRDUDE_OPTS) -p $(MCU_AVRDUDE) -U flash:r:flash.bin:r -U boot:r:boot.bin:r -U usersig:r:usersig.bin:r -c $(AVRDUDE_PGMR)

fuseread:
	-@rm -f fuse
	-$(AVRDUDE) $(AVRDUDE_OPTS) -p $(MCU_AVRDUDE) -U fuse:r:fuse:h -c $(AVRDUDE_PGMR) >/dev/null 2>&1
	-@cat fuse
	-$(AVRDUDE) $(AVRDUDE_OPTS) -p $(MCU_AVRDUDE) -U lfuse:r:fuse:h -c $(AVRDUDE_PGMR) >/dev/null 2>&1
	-@cat fuse
	-$(AVRDUDE) $(AVRDUDE_OPTS) -p $(MCU_AVRDUDE) -U hfuse:r:fuse:h -c $(AVRDUDE_PGMR) >/dev/null 2>&1
	-@cat fuse
	-$(AVRDUDE) $(AVRDUDE_OPTS) -p $(MCU_AVRDUDE) -U efuse:r:fuse:h -c $(AVRDUDE_PGMR) >/dev/null 2>&1
	-@cat fuse

chiperase:
	$(AVRDUDE) $(AVRDUDE_OPTS) -p $(MCU_AVRDUDE) -e -c $(AVRDUDE_PGMR)

eepromread:
	$(AVRDUDE) $(AVRDUDE_OPTS) -p $(MCU_AVRDUDE) -U eeprom:r:eeprom:r -c $(AVRDUDE_PGMR)

eepromerase:
	rm -f empty
	python -c 'open("empty", "wb").write(chr(255) * 2048)'
	$(AVRDUDE) $(AVRDUDE_OPTS) -p $(MCU_AVRDUDE) -e -U eeprom:w:empty:r -c $(AVRDUDE_PGMR)
	rm -f empty

sramlayout: $(PROJNAME)
	@$(NM) -n -f posix -t x $(PROJNAME)	| grep -E '^[^ ]+ . 0080[0-9a-f]{4} ' | awk '\
		BEGIN {\
			printf("Addr. Hex/Dec   | Addr. Hex/Dec   | Symbol Type                                 Name | Size | Total | Remaining\n");\
			REMAINING = $(SRAM_SIZE);\
			TOTAL = 0;\
		}\
		/^_edata/ {\
			OFFSET = strtonum("0x" $$3) - 0x800000;\
			START_DATA = OFFSET;\
		}\
		/^[^_]/ {\
			SYMBOL = $$1;\
			SYMBOLTYPE = $$2;\
			OFFSET = strtonum("0x" $$3) - 0x800000;\
			SIZE = strtonum("0x" $$4);\
			REMAINING -= SIZE;\
			TOTAL += SIZE;\
			printf("0x%-5x %6d  | 0x%-5x %6d  | %s  %45s | %4d | %5d | %5d\n", OFFSET, OFFSET, OFFSET - START_DATA, OFFSET - START_DATA, SYMBOLTYPE, SYMBOL, SIZE, TOTAL, REMAINING);\
	  	}\
	'

sramlayout-ss: $(PROJNAME)
	@$(NM) --size-sort -n -f posix -t x $(PROJNAME)	| grep -E '^[^ ]+ . 0080[0-9a-f]{4} ' | awk '\
		BEGIN {\
			printf("Addr. Hex/Dec   | Addr. Hex/Dec   | Symbol Type                                 Name | Size | Total | Remaining\n");\
			REMAINING = $(SRAM_SIZE);\
			TOTAL = 0;\
		}\
		/^_edata/ {\
			OFFSET = strtonum("0x" $$3) - 0x800000;\
			START_DATA = OFFSET;\
		}\
		/^[^_]/ {\
			SYMBOL = $$1;\
			SYMBOLTYPE = $$2;\
			OFFSET = strtonum("0x" $$3) - 0x800000;\
			SIZE = strtonum("0x" $$4);\
			REMAINING -= SIZE;\
			TOTAL += SIZE;\
			printf("0x%-5x %6d  | 0x%-5x %6d  | %s  %45s | %4d | %5d | %5d\n", OFFSET, OFFSET, OFFSET - START_DATA, OFFSET - START_DATA, SYMBOLTYPE, SYMBOL, SIZE, TOTAL, REMAINING);\
	  	}\
	'

flashlayout-ss: $(PROJNAME)
	@$(NM) --size-sort -n -f posix -t x $(PROJNAME) | grep -E '^[^. ]+ [Tt] 0000[0-9a-f]{4} ' | grep -v '^_' | awk '\
		BEGIN {\
			printf("Addr. Hex/Dec   | Symbol Type                                 Name | Size | Total | Remaining\n");\
			REMAINING = $(FLASH_SIZE);\
			TOTAL = 0;\
		}\
		// {\
			SYMBOL = $$1;\
			SYMBOLTYPE = $$2;\
			OFFSET = strtonum("0x" $$3);\
			SIZE = strtonum("0x" $$4);\
			REMAINING -= SIZE;\
			TOTAL += SIZE;\
			printf("0x%-5x %6d  | %s  %45s | %4d | %5d | %5d\n", OFFSET, OFFSET, SYMBOLTYPE, SYMBOL, SIZE, TOTAL, REMAINING);\
	  	}\
	'

flashlayout: $(PROJNAME)
	@$(NM) -n -f posix -t x $(PROJNAME) | grep -E '^[^. ]+ [Tt] 0000[0-9a-f]{4} ' | grep -v '^_' | awk '\
		BEGIN {\
			printf("Addr. Hex/Dec   | Symbol Type                                 Name | Size | Total | Remaining\n");\
			REMAINING = $(FLASH_SIZE);\
			TOTAL = 0;\
		}\
		// {\
			SYMBOL = $$1;\
			SYMBOLTYPE = $$2;\
			OFFSET = strtonum("0x" $$3);\
			SIZE = strtonum("0x" $$4);\
			REMAINING -= SIZE;\
			TOTAL += SIZE;\
			printf("0x%-5x %6d  | %s  %45s | %4d | %5d | %5d\n", OFFSET, OFFSET, SYMBOLTYPE, SYMBOL, SIZE, TOTAL, REMAINING);\
	  	}\
	'

gdb: $(PROJNAME)
	avr-gdb --eval-command "target remote :10001" --eval-command "init" $(PROJNAME)

###################################################################################################

$(PROJNAME).S: $(PROJNAME).c
	$(CC) $(CFLAGS) -S -o $(PROJNAME).S $(PROJNAME).c

$(PROJNAME).E: $(PROJNAME).c
	$(CC) $(CFLAGS) -E -o $(PROJNAME).E $(PROJNAME).c

$(PROJNAME).syms: $(PROJNAME).c
	$(CC) $(CFLAGS) -E -dM -o $(PROJNAME).syms $(PROJNAME).c

$(PROJNAME): $(PROJNAME).c $(OBJS) $(LIBOBJS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $(PROJNAME) $(PROJNAME).c $(OBJS) $(LIBOBJS)

$(PROJNAME)_Flash.hex: $(PROJNAME)
	$(OBJCOPY) -R .eeprom -O ihex --gap-fill=0xff $(PROJNAME) $(PROJNAME)_Flash.hex

$(PROJNAME)_EEPROM.hex: $(PROJNAME)
	-$(OBJCOPY) -j .eeprom -O ihex --gap-fill=0xff $(PROJNAME) $(PROJNAME)_EEPROM.hex

$(PROJNAME).bin: $(PROJNAME)
	$(OBJCOPY) -R .eeprom -O binary --gap-fill=0xff $(PROJNAME) $(PROJNAME).bin
	@chmod 644 $(PROJNAME).bin

$(PROJNAME).dmp: $(PROJNAME)
	$(OBJDUMP) -d $(PROJNAME) > $(PROJNAME).dmp
	@$(SIZE) -B $(PROJNAME) | tail -n 1 | awk '\
		{\
			USED = $$1;\
			printf("%d bytes of flash used for project $(PROJNAME) (%.1f%%, %d Bytes remaining)\n", USED, USED / $(FLASH_SIZE).0 * 100, $(FLASH_SIZE) - USED);\
		}\
	'

$(PROJNAME).coff: $(PROJNAME) $(PROJNAME)_Flash.hex
	$(OBJCOPY) --debugging --change-section-address .data-0x800000 --change-section-address .bss-0x800000 --change-section-address .noinit-0x800000 --change-section-address .eeprom-0x810000 -O coff-avr $< $@

%.o: %.S
	$(CC) $(CFLAGS) -c -o $@ $<

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

%.o: %.s
	$(CC) $(CFLAGS) -c -o $@ $<

