/*
 * Copyright (c) 2015 Jérémie DECOCK <jd.jdhp@gmail.com> (www.jdhp.org)
 */

#include <avr/io.h>           // Defines pins, ports, etc.

#include "uart_util.h"

/*
 * See also:
 * - https://github.com/hexagon5un/AVR-Programming/blob/master/Chapter05_Serial-IO/serialLoopback/serialLoopback.c
 * - http://www.appelsiini.net/2011/simple-usart-with-avr-libc#registers
 */

int main(void) {

    uart_init();

    char c;

    while(1) {
        c = uart_read_char();

        uart_send_char('.');
        uart_send_char(c);
    }

    return(0);
}
