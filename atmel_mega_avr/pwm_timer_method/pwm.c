/*
 * Copyright (c) 2015 Jérémie DECOCK <jd.jdhp@gmail.com> (www.jdhp.org)
 */

#include <avr/io.h>           // Defines pins, ports, etc
#include <util/delay.h>       // Functions to waste time

int main(void) {

    // INIT PB5 AS OUTPUT (LED) /////////////////////////////////////
    
    DDRB = (1 << DDB3);         // DDRB is the Data Direction Register B: we set pin PB3 (DDB3) as an output


    // INIT TIMER 2 (with the 8 bits counter) ///////////////////////
    
    // Mode 3: Fast PWM (cf. datasheet p153 and 156), TOP=0xFF
    TCCR2A |= (1 << WGM20);
    TCCR2A |= (1 << WGM21);  // Waveform generation mode

    // Frequency
    TCCR2B |= (1 << CS21);   // Setup PWM Freq = F_CPU/8/256

    // Output mode (setup PWM output on OCR2A)
    TCCR2A |= (1 << COM2A1); // Clear OC2A (PB3) on compare match, set OC2A at BOTTOM.
                             // The PWM turns the pin ON when it overflows from 255 to 0,
                             // and turn it OFF when it reaches the compare value (brightness).


    // EVENT LOOP ///////////////////////////////////////////////////
    
    uint8_t brightness = 0;

    while(1) {
        OCR2A = brightness;
        brightness++;

        _delay_ms(10);
    }

    return(0);
}
