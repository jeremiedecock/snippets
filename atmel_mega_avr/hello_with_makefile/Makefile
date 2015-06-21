# Copyright (c) 2015 Jérémie Decock

NAME = blink_led
TARGET = $(NAME).hex

# TOOLCHAIN SETUP #####################

CC = avr-gcc
OBJ2HEX = avr-objcopy 
FLASH = avrdude

# MCU SETUP ###########################

# For a complete list of supported chips, type "avr-gcc --target-help" and
# search the "Known MCU names" section.
AVRGCC_MCU_ID = atmega328p

# The clock speed of the MCU.
# Without external clock source (cristal), this should be 1000000UL (1MHz) or
# 8000000UL (8MHz) for ATMega MCUs.
# The right value is required for UART serial communications, ...
F_CPU = 1000000UL

#AVRDUDE_PROGRAMMER_ID = avrisp
#AVRDUDE_PROGRAMMER_ID = avrispv2
#AVRDUDE_PROGRAMMER_ID = usbtiny
AVRDUDE_PROGRAMMER_ID = usbasp

#AVRDUDE_MCU_ID = t85
AVRDUDE_MCU_ID = m328p
#AVRDUDE_MCU_ID =

AVRDUDE_PORT = /dev/ttyUSB0

FLASH_OPTIONS = 

#######################################

CFLAGS = -g -Wall
LIBS = 

OBJS = $(patsubst %.c,%.o,$(wildcard *.c))

.PHONY : all flash clean init

all : $(TARGET)

#######################################

# COMPILE (MAKE .o OBJECT FILES)
%.o : %.c
	$(CC) $(CFLAGS) -Os -mcall-prologues -mmcu=$(AVRGCC_MCU_ID) -DF_CPU=$(F_CPU) -o $@ -c $<

# LINK (MAKE THE ELF BINARY FILE)
$(NAME).elf : $(OBJS)
	$(CC) $(CFLAGS) -mmcu=$(AVRGCC_MCU_ID) -o $@ $^ $(LIBS)

# CONVERT TO INTEL HEX FORMAT
$(TARGET) : $(NAME).elf
	$(OBJ2HEX) -j .text -j .data -O ihex $< $@

# PROGRAM (FLASH) THE AVR MCU
# -c the type of flash programmer that you are using.
# -p the type of AVR chip that you are using.
# -P the serial port the programmer is connected to.
# -b the baud rate for serial programmers.
# -U reads or writes to memory.
flash : $(TARGET)
	$(FLASH) -c $(AVRDUDE_PROGRAMMER_ID) -p $(AVRDUDE_MCU_ID) -P $(AVRDUDE_PORT) $(FLASH_OPTIONS) -e -U flash:w:$(TARGET)

#######################################

clean :
	rm -vf *.o *.elf *.ihex *.oct *.bin *.raw *.motorola

init : clean
	rm -vf $(TARGET)
