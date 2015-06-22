#include <avr/io.h>           // Defines pins, ports, etc.

int main(void) {

    DDRB |=  (1<<DDB5);       // DDRB is the Data Direction Register B: we set pin5 (DDB5 = PB5) as an output.
    DDRD &= ~(1<<DDD2);       // DDRD is the Data Direction Register D: we set pin2 (DDD2 = PD2) as an input.

    PORTB &= ~(1<<DDB5);      // Switch off the LED on the output pin PB5
    PORTD |=  (1<<DDD2);      // Set pull-up resistor on the input pin PD2

    while(1) {

        if(PIND & (1<<DDD2)) {
            // PD2 = 1, the button is RELEASED
            PORTB &= ~(1<<DDB5);  // Switch OFF pin5 (DDB5) with the XOR operator
        } else {
            // PD2 = 0, the button is PRESSED
            PORTB |= (1<<DDB5);   // Switch ON pin5 (DDB5) with the XOR operator
        }

    }

    return(0);                // This line is never reached...
}
