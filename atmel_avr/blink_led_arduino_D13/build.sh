#!/bin/sh

#avr-gcc --target-help
#AVRGCC_MCU_ID=attiny85
#AVRGCC_MCU_ID=atmega328
AVRGCC_MCU_ID=atmega328p
#AVRGCC_MCU_ID=

# COMPILE (MAKE .o OBJECT FILES)
avr-gcc -g -Wall -Os -mcall-prologues -mmcu=${AVRGCC_MCU_ID} -c blink_led.c

# LINK (MAKE THE ELF BINARY FILE)
avr-gcc -g -mmcu=${AVRGCC_MCU_ID} -o blink_led.elf blink_led.o

# CONVERT TO INTEL HEX FORMAT
# doc pololu: objcopy -R .eeprom -O ihex blink_led.elf blink_led.hex
avr-objcopy -j .text -j .data -O ihex blink_led.elf blink_led.hex

