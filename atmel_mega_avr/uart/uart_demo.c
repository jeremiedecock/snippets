#include <avr/io.h>           /* Defines pins, ports, etc */
#include <util/delay.h>       /* Functions to waste time */

#include "uart_util.h"

/*
 * See also:
 * - https://github.com/hexagon5un/AVR-Programming/blob/master/Chapter05_Serial-IO/serialLoopback/serialLoopback.c
 * - http://www.appelsiini.net/2011/simple-usart-with-avr-libc#registers
 */

int main(void) {

    uart_init();

    DDRB = (1<<DDB5);         // DDRB is the Data Direction Register B: we set pin5 (DDB5) as an output
                              // DDB5 is just a constant equals to 5 (DDB3=3, DDC3=3, DDD3=3, ...)

    PORTB &= ~(1<<DDB5);      // Turn off pin 5 (DDB5)

    char c = '.';

    while(1) {
        uart_putchar(c);
        PORTB ^= (1<<DDB5);   // Toggle pin5 (DDB5) with the XOR operator
        _delay_ms(1000);      // wait 1000ms
    }

    return(0);                // This line is never reached...
}
