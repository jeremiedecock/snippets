// TODO: ?????
#define F_CPU 1000000UL
// TODO: ?????
//#define F_CPU 8000000UL

#include <avr/io.h>           /* Defines pins, ports, etc */
#include <util/delay.h>       /* Functions to waste time */

int main(void) {

    // On Arduino Duemilanove, the embeded LED is on pin D13 (PB5/SCK with AVR notation)

    DDRB = (1<<DDB5);         // Data Direction Register B: pin5 is an output

    PORTB &= ~(1<<DDB5);      // Turn off DDB5 (AND NOT)

    while(1) {
        PORTB ^= (1<<DDB5);   // Toggle DDB5   (XOR)
        _delay_ms(1000);       // wait
    }

    return(0);                // This line is never reached...
}
