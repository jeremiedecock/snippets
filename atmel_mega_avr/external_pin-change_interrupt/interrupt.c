/*
 * Copyright (c) 2015 Jérémie DECOCK <jd.jdhp@gmail.com> (www.jdhp.org)
 */

#include <avr/io.h>           // Defines pins, ports, etc.
#include <util/delay.h>
#include <avr/interrupt.h>

// Interrupt Service Routine
// Executed every time there is a change on button
// ISR and PCINT2_vect are macros defined in avr/interrupt.h
// PCINT0 covers interrupts for pins PB0 to PB7
// PCINT1 covers interrupts for pins PC0 to PC6
// PCINT2 covers interrupts for pins PD0 to PD7
ISR(PCINT2_vect) {
    if(PIND & (1<<DDD2)) {
        // PD2 = 1, the button is RELEASED
        PORTB &= ~(1<<DDB5);  // Switch OFF pin5 (DDB5)
    } else {
        // PD2 = 0, the button is PRESSED
        PORTB |= (1<<DDB5);   // Switch ON pin5 (DDB5)
    }
}

int main(void) {

    // Init PB5 as output (LED)
    DDRB |=  (1<<DDB5);       // DDRB is the Data Direction Register B: we set pin PB5 (DDB5 = PB5) as an output
    PORTB &= ~(1<<DDB5);      // Switch off the LED on the output pin PB5

    // Init PD2 (INT0) as input (button)
    DDRD &= ~(1<<DDD2);       // DDRD is the Data Direction Register D: we set pin PD2 (DDD2 = PD2) as an input
    PORTD |=  (1<<DDD2);      // Set pull-up resistor on the input pin PD2
    
    // Init interrupt INT0
    PCICR |= (1 << PCIE2);    // Activate pin-change interrupt for bank D pins
    PCMSK2 |= (1 << PCINT18); // Set mask to look only for PCINT18 / PD2 in bank D pins
    sei();                    // Set (global) interrupt enable bit

    while(1) {

        // Do something...

        _delay_ms(10);
    }

    return(0);
}
