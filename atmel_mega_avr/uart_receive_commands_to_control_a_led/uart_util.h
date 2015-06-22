#ifndef UART_UTIL_H
#define UART_UTIL_H

#ifndef BAUD      // If not defined in Makefile...
#define BAUD 9600 // Set a safe default baud rate
#endif

void uart_init(void);

void uart_putchar(char c);

char uart_getchar(void);

#endif /* UART_UTIL_H */
