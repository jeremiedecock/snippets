/*
 * Led: a led blinking snippet for Arduino Duemilanove (ATMEGA328).
 *      Blink embeded led "L" (arduino's digital pin 13): the 6th bit of PORTB
 *      (called PB5).
 *
 * Copyright (c) 2013 Jérémie Decock
 * * Usage:
 *    avr-gcc -Os -DF_CPU=16000000UL -mmcu=atmega328p -c -o led.o led.c
 *    avr-gcc -mmcu=atmega328p led.o -o led.elf
 *    avr-objcopy -O ihex -R .eeprom led.elf led.hex
 *    avrdude -carduino -patmega328p -P/dev/ttyUSB0 -b57600 -D -Uflash:w:led.hex
 * 
 * Required packages (Debian):
 * - gcc-avr : the GNU C compiler, ported to the AVR architecture
 * - avr-libc : a library giving access to special functions of the AVR
 * - binutils-avr : tools for converting objects code into hex files
 * - avrdude : the software to drive the programmer
 *
 * See: http://arduino.cc/en/Hacking/PinMapping168
 *      http://forums.trossenrobotics.com/tutorials/introduction-129/avr-basics-3261/
 *      http://openhardwareplatform.blogspot.fr/2011/03/inside-arduino-build-process.html
 *
 */

#include <avr/io.h>
#include <util/delay.h>

int main (void)
{
    /* 
     * DDRB is the data-direction register, which defines whether each pin is
     * an input (0) or an output (1). If we set DDRB = 0x0F, our upper four
     * pins (PB4-PB7) are set as inputs, while our lower four pins (PB0-PB3)
     * are outputs.
     */
    DDRB = 0xFF;

    while(1) {

        PORTB = 0x20;    // switch led (6th bit of PORTB called PB5)
        _delay_ms(1000); // wait 1 second

        PORTB = 0x00;    // switch led off
        _delay_ms(1000); // wait 1 second

    }

    return 0;
}

