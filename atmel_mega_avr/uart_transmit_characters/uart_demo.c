#include <avr/io.h>           // Defines pins, ports, etc.
#include <util/delay.h>       // Functions to waste time

#include "uart_util.h"

/*
 * See also:
 * - https://github.com/hexagon5un/AVR-Programming/blob/master/Chapter05_Serial-IO/serialLoopback/serialLoopback.c
 * - http://www.appelsiini.net/2011/simple-usart-with-avr-libc#registers
 */

int main(void) {

    uart_init();

    char c = '.';

    while(1) {
        uart_send_char(c);    // Send a character to UART

        _delay_ms(1000);      // Wait 1000ms
    }

    return(0);
}
