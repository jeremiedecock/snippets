#include <avr/io.h>       // Defines pins, ports, etc.

#include "uart_util.h"

#include <util/setbaud.h>


// INIT UART FUNCTION /////////////////////////////////////////////////////////
// No parity, 8 data bits, 1 stop bit.

void uart_init(void) {

    // Set UART speed
    UBRR0H = UBRRH_VALUE; // UBRRH_VALUE is defined in util/setbaud.h
    UBRR0L = UBRRL_VALUE; // UBRRL_VALUE is defined in util/setbaud.h

    // Determine if UART has to be configured to run in double speed mode
#if USE_2X
    UCSR0A |= (1 << U2X0);  // U2X0 is defined in util/setbaud.h
#else
    UCSR0A &= ~(1 << U2X0); // U2X0 is defined in util/setbaud.h
#endif

    // Set frame format: 8 data bits and 1 stop bit
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
    
    // Enable receiver (RXD) and transmitter (TXD)
    UCSR0B = (1 << TXEN0) | (1 << RXEN0);
}

// TRANSMIT ONE BYTE FUNCTION /////////////////////////////////////////////////

void uart_send_char(char c) {
    loop_until_bit_is_set(UCSR0A, UDRE0); // Wait until data register empty
    UDR0 = c;                             // Transmit data to UART by writing a byte to USART Data Register UDR0
}

// TRANSMIT A STRING FUNCTION /////////////////////////////////////////////////

void uart_send_string(const char str[]) {
    uint8_t i = 0;
    while(str[i] != '\0') {
        uart_send_char(str[i]);
        i++;
    }
}

// READ ONE BYTE FUNCTION /////////////////////////////////////////////////////

char uart_read_char(void) {
    loop_until_bit_is_set(UCSR0A, RXC0);  // Wait until data exists
    return UDR0;
}
