/*
 * Copyright (c) 2015 Jérémie DECOCK <jd.jdhp@gmail.com> (www.jdhp.org)
 */

#include <avr/io.h>           // Defines pins, ports, etc
#include <util/delay.h>       // Functions to waste time

// LED delay in microseconds
#define LED_DELAY 20

void pwm_pb5(uint8_t brightness) {

    PORTB |= (1<<DDB5);               // Turn on the pin

    uint8_t i;
    for(i = 0 ; i < 255 ; i++) {      // PWM frequency = 256 ; "Duty cytle" = brightness
        if(i >= brightness) {         // Once it's been on long enough
            PORTB &= ~(1 << DDB5);    // Turn off the pin
        }
        _delay_us(LED_DELAY);
    }
}

int main(void) {

    DDRB = (1<<DDB5);         // DDRB is the Data Direction Register B: we set pin5 (DDB5) as an output

    uint8_t brightness = 0;

    while(1) {
        pwm_pb5(brightness);
        brightness++;
    }

    return(0);
}
