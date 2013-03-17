#!/bin/sh

# Compile and flash led.c for Arduino Duemilanove (ATMEGA328)

# To see actual commands used by arduino IDE:
#   strace -oarduino.log -f -s512 arduino
# then search execve syscall in arduino.log

# Required packages (Debian):
# - gcc-avr : the GNU C compiler, ported to the AVR architecture
# - avr-libc : a library giving access to special functions of the AVR
# - binutils-avr : tools for converting objects code into hex files
# - avrdude : the software to drive the programmer

# Compile led.c
#   -DF_CPU=16000000UL -> define macro F_CPU
echo "Compile"
avr-gcc -Os -DF_CPU=16000000UL -mmcu=atmega328p -c -o led.o led.c
avr-gcc -mmcu=atmega328p led.o -o led.elf

# Translate object file
#   -O -> output target (output object format)
#   -R -> remove section ...
echo "Translate"
avr-objcopy -O ihex -R .eeprom led.elf led.hex
avr-size led.hex
#avr-objcopy -O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load --no-change-warnings --change-section-lma .eeprom=0 led.elf led.eep

# Flash the AVR MCU
#   -c -> programmer-id
#   -p -> ?
#   -P -> port
#   -b -> baudrate
#   -U -> memtype:op:filename[:fileformat]
echo "Flash"
avrdude -carduino -patmega328p -P/dev/ttyUSB0 -b57600 -D -Uflash:w:led.hex
#avrdude -carduino -patmega328p -P/dev/ttyUSB0 -b57600 -D -Uflash:w:led.eep

