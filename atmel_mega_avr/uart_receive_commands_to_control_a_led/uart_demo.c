#include <avr/io.h>           // Defines pins, ports, etc.
#include <util/delay.h>       // Functions to waste time

#include "uart_util.h"

/*
 * See also:
 * - https://github.com/hexagon5un/AVR-Programming/blob/master/Chapter05_Serial-IO/serialLoopback/serialLoopback.c
 * - http://www.appelsiini.net/2011/simple-usart-with-avr-libc#registers
 */

char switch_on_char = 'i';
char switch_off_char = 'o';

int main(void) {

    uart_init();

    DDRB = (1<<DDB5);         // DDRB is the Data Direction Register B: we set pin5 (DDB5) as an output
                              // DDB5 is just a constant equals to 5 (DDB3=3, DDC3=3, DDD3=3, ...)

    PORTB &= ~(1<<DDB5);      // Turn off pin 5 (DDB5)

    char cmd;

    while(1) {
        cmd = uart_getchar(); // Get a character from UART

        if(cmd == switch_on_char) {
            PORTB |= (1<<DDB5);    // Switch ON pin5 (DDB5)
        } else if(cmd == switch_off_char) {
            PORTB &= ~(1<<DDB5);   // Switch OFF pin5 (DDB5)
        }
    }

    return(0);
}
