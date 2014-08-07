// TODO: ?????
//#define F_CPU 1000000UL
// TODO: ?????
#define F_CPU 8000000UL

#include <avr/io.h>           /* Defines pins, ports, etc */
#include <util/delay.h>       /* Functions to waste time */

int main(void) {

    // On 3Pi, the embeded LED is on pin PD1

    DDRD = (1<<DDD1);         // Data Direction Register B: pin5 is an output

    PORTD &= ~(1<<DDD1);      // Turn off DDD1 (AND NOT)

    while(1) {
        PORTD ^= (1<<DDD1);   // Toggle DDD1   (XOR)
        _delay_ms(8000);      // wait
    }

    return(0);                // This line is never reached...
}
