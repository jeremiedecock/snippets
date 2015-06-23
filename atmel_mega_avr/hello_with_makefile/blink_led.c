/*
 * Copyright (c) 2015 Jérémie DECOCK <jd.jdhp@gmail.com> (www.jdhp.org)
 */

#include <avr/io.h>           // Defines pins, ports, etc
#include <util/delay.h>       // Functions to waste time

int main(void) {

    // On Arduino Duemilanove, the embeded LED is on pin D13 (PB5/SCK with AVR notation)

    DDRB = (1<<DDB5);         // DDRB is the Data Direction Register B: we set pin5 (DDB5) as an output
                              // DDB5 is just a constant equals to 5 (DDB3=3, DDC3=3, DDD3=3, ...)

    PORTB &= ~(1<<DDB5);      // Turn off pin 5 (DDB5)

    while(1) {
        PORTB ^= (1<<DDB5);   // Toggle pin5 (DDB5) with the XOR operator
        _delay_ms(1000);      // wait 1000ms
    }

    return(0);                // This line is never reached...
}
