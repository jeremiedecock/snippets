/*
 * Copyright (c) 2015 Jérémie DECOCK <jd.jdhp@gmail.com> (www.jdhp.org)
 */

#include <avr/io.h>           // Defines pins, ports, etc

int main(void) {

    // INIT PB5 AS OUTPUT (LED) /////////////////////////////////////
    
    DDRB = (1<<DDB5);         // DDRB is the Data Direction Register B: we set pin5 (DDB5) as an output
    PORTB &= ~(1<<DDB5);      // Turn off pin 5 (DDB5)
    
    // INIT TIMER 1 (the one with the 16 bits counter) //////////////
    // REM: TCNT0 (timer 0) and TCNT2 (timer 2) are 8 bits conters

    // Normal mode (nothing to setup)
    
    // Clock speed = 1 MHz / 64
    TCCR1B |= (1 << CS11) | (1 << CS10); // Each tick is 64 microseconds ~= 15.6 per ms
                                         
    // No special output modes (nothing to setup)
    
    // Reset counter value
    TCNT1 = 0;

    /////////////////////////////////////////////////////////////////

    uint16_t timer_value;
    
    while(1) {
        timer_value = TCNT1 >> 4;  // Each tick is approx 1/16 milliseconds, so we bit-shift divide

        if(timer_value >= 1000) {  // Every second (1000ms) do...
            PORTB ^= (1<<DDB5);    // Toggle pin5 (DDB5) with the XOR operator
            TCNT1 = 0;             // Reset counter value
        }
    }

    return(0);
}
