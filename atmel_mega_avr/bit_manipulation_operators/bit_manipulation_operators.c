/*
 * Copyright (c) 2014,2015 Jérémie DECOCK (http://www.jdhp.org)
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include<stdio.h>

#define BYTE_TO_BINARY_PATTERN "%d%d%d%d%d%d%d%d"
#define BYTE_TO_BINARY(byte)  \
      (byte & 0x80 ? 1 : 0), \
      (byte & 0x40 ? 1 : 0), \
      (byte & 0x20 ? 1 : 0), \
      (byte & 0x10 ? 1 : 0), \
      (byte & 0x08 ? 1 : 0), \
      (byte & 0x04 ? 1 : 0), \
      (byte & 0x02 ? 1 : 0), \
      (byte & 0x01 ? 1 : 0) 

void print_bin(char x) {
    printf("bin: "BYTE_TO_BINARY_PATTERN"\n", BYTE_TO_BINARY(x));
    //printf("hex: %#x\n", x);
    //printf("dec: %d\n", x);
    printf("\n");
}

int main(void) {
    
    char x, y;
    
    // 0bXX notation is a GNU extension (https://gcc.gnu.org/onlinedocs/gcc/Binary-constants.html)
    x = 0b00011010;   
    y = 0b00000011;   

    printf("x:\n");
    print_bin(x);

    printf("y:\n");
    print_bin(y);

    // AND
    printf("LOGICAL AND: x&y\n");
    print_bin(x&y);
    
    // OR
    printf("LOGICAL OR: x|y\n");
    print_bin(x|y);
    
    // XOR
    printf("LOGICAL XOR: x^y\n");
    print_bin(x^y);
    
    // NOT
    printf("LOGICAL NOT: ~x\n");
    print_bin(~x);
    
    // LEFT SHIFT (1 BIT)
    printf("LEFT SHIFT (1 BIT): x<<1\n");
    print_bin(x<<1);
    
    // RIGHT SHIFT (1 BIT)
    printf("RIGHT SHIFT (1 BIT): x>>1\n");
    print_bin(x>>1);
    
    // LEFT SHIFT (2 BIT)
    printf("LEFT SHIFT (2 BIT): x<<2\n");
    print_bin(x<<2);
    
    // RIGHT SHIFT (2 BIT)
    printf("RIGHT SHIFT (2 BIT): x>>2\n");
    print_bin(x>>2);

    // SET A BIT ////////////////////////////////

    int N, M;

    printf("x:\n");
    print_bin(x);

    // SET THE Nth BIT OF x TO 1
    N = 2;
    printf("SET THE Nth BIT OF x TO 1 (WITH HERE N=2 IE THE THIRD BIT)\n");
    printf("- LONG VERSION:  x  = x | (1<<N)\n");
    printf("- SHORT VERSION: x |= (1<<N)\n");
    printf("USUALLY, x IS PORTB, PORTC or PORTD\n");
    print_bin(x | (1<<N));

    // SET THE Nth BIT OF x TO 0
    N = 3;
    printf("SET THE Nth BIT OF x TO 0 (WITH HERE N=3 IE THE FOURTH BIT)\n");
    printf("- LONG VERSION:  x  = x & ~(1<<N)\n");
    printf("- SHORT VERSION: x &= ~(1<<N)\n");
    printf("USUALLY, x IS PORTB, PORTC or PORTD\n");
    print_bin(x & ~(1<<N));

    // SET THE Nth AND THE Mth BIT OF x TO 1
    N = 2;
    M = 0;
    printf("SET THE Nth AND THE Mth BIT OF x TO 1 (WITH HERE N=2 IE THE THIRD BIT AND M=0 IE THE FIRST BIT)\n");
    printf("- LONG VERSION:  x  = x | ( (1<<N)|(1<<M) )\n");
    printf("- SHORT VERSION: x |= (1<<N)|(1<<M)\n");
    printf("USUALLY, x IS PORTB, PORTC or PORTD\n");
    print_bin(x | ( (1<<N)|(1<<M) ));

    // SET THE Nth AND THE Mth BIT OF x TO 0
    N = 3;
    M = 1;
    printf("SET THE Nth AND THE Mth BIT OF x TO 0 (WITH HERE N=3 IE THE FOURTH BIT AND M=1 IE THE SECOND BIT)\n");
    printf("- LONG VERSION:  x  = x & ~( (1<<N)|(1<<M) )\n");
    printf("- SHORT VERSION: x &= ~( (1<<N)|(1<<M) )\n");
    printf("USUALLY, x IS PORTB, PORTC or PORTD\n");
    print_bin(x & ~( (1<<N)|(1<<M) ));

    // TEST A BIT ///////////////////////////////

    printf("x:\n");
    print_bin(x);

    // TEST THE Nth BIT OF x
    N = 2;
    printf("TEST THE Nth BIT OF x (WITH HERE N=2 IE THE THIRD BIT)\n");
    printf("res = x & (1<<N)\n");
    printf("USUALLY, x IS PORTB, PORTC or PORTD\n");
    if(x & (1<<N)) printf(">>> true\n");
    else printf(">>> false\n");
    printf("\n");

    // TOGGLE A BIT /////////////////////////////

    printf("x:\n");
    print_bin(x);

    // TEST THE Nth BIT OF x
    N = 2;
    printf("TOGGLE THE Nth BIT OF x (WITH HERE N=2 IE THE THIRD BIT)\n");
    printf("- LONG VERSION:  x  = x ^ (1<<N)\n");
    printf("- SHORT VERSION: x ^= (1<<N)\n");
    printf("USUALLY, x IS PORTB, PORTC or PORTD\n");
    print_bin(x ^ (1<<N));

    // TEST THE Nth AND THE Mth BIT OF x
    N = 2;
    M = 1;
    printf("TOGGLE THE Nth AND THE Mth BIT OF x (WITH HERE N=2 IE THE THIRD BIT AND M=1 IE THE SECOND BIT)\n");
    printf("- LONG VERSION:  x  = x ^ ( (1<<N)|(1<<M) )\n");
    printf("- SHORT VERSION: x ^= (1<<N)|(1<<M)\n");
    printf("USUALLY, x IS PORTB, PORTC or PORTD\n");
    print_bin(x ^ ( (1<<N)|(1<<M) ));

    return 0;
}
