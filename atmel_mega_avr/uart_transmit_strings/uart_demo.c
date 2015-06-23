/*
 * Copyright (c) 2015 Jérémie DECOCK <jd.jdhp@gmail.com> (www.jdhp.org)
 */

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

    while(1) {
        uart_send_string("Hello World!\r\n");  // Send a character to UART

        _delay_ms(1000);      // Wait 1000ms
    }

    return(0);
}
