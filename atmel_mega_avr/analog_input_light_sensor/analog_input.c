/*
 * Copyright (c) 2015 Jérémie DECOCK <jd.jdhp@gmail.com> (www.jdhp.org)
 */

#include <avr/io.h>           // Defines pins, ports, etc.
#include <util/delay.h>       // Functions to waste time
#include <stdio.h>            // For the snprintf function

#include "uart_util.h"

void adc0_init(void) {
    ADMUX |= (1 << REFS0);  // Reference voltage on AVCC
    ADCSRA |= (1 << ADPS2); // ADC clock prescaler /16
    ADCSRA |= (1 << ADEN);  // Enable ADC
}

int main(void) {

    uart_init();
    adc0_init();

    uint16_t adc_value;
    char adc_value_str[5];

    while(1) {

        // Get the ADC value
        ADCSRA |= (1 << ADSC);                 // Start ADC conversion
        loop_until_bit_is_clear(ADCSRA, ADSC); // Wait until done
        adc_value = ADC;                       // Read ADC in

        // Send the value to UART
        snprintf((char *) &adc_value_str, 5, "%d", adc_value);
        uart_send_string(adc_value_str);       // Send a string to UART
        uart_send_string("\r\n");              // Send a string to UART

        // Wait
        _delay_ms(1000);      // Wait 1000ms

    }

    return(0);
}
