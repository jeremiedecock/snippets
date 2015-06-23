/*
 * Copyright (c) 2015 Jérémie DECOCK <jd.jdhp@gmail.com> (www.jdhp.org)
 */

#include <avr/io.h>           // Defines pins, ports, etc.
#include <util/delay.h>

#include <stdbool.h>          // C99 boolean type

/* Microseconds */
#define DEBOUNCE_TIME 5

/**
 * Check if the button PD2 is pressed.
 * Use a basic debounce routine.
 */
bool button_is_pressed(void) {

    if((PIND & (1<<DDD2)) == 0) {

        // PD2 = 0, the button is PRESSED
        _delay_ms(DEBOUNCE_TIME);

        if((PIND & (1<<DDD2)) == 0) {
            // PD2 = 0, the button is still PRESSED
            return true;
        }

    }

    return false;
}

int main(void) {

    DDRB |=  (1<<DDB5);       // DDRB is the Data Direction Register B: we set pin5 (DDB5 = PB5) as an output
    DDRD &= ~(1<<DDD2);       // DDRD is the Data Direction Register D: we set pin2 (DDD2 = PD2) as an input

    PORTB &= ~(1<<DDB5);      // Switch off the LED on the output pin PB5
    PORTD |=  (1<<DDD2);      // Set pull-up resistor on the input pin PD2

    bool button_was_pressed = false;

    while(true) {

        if(button_is_pressed()) {
            
            if(!button_was_pressed) {
                PORTB ^= (1<<DDB5);   // Toggle pin5 (DDB5) with the XOR operator
                button_was_pressed = true;
            }

        } else {
            
            button_was_pressed = false;

        }

    }

    return(0);
}
