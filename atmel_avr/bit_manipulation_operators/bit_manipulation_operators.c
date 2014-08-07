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
    printf("hex: %#x\n", x);
    printf("dec: %d\n", x);
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

    /////////////////////////////////////////////

    //PORTB ^= (1<<DDB0);
    printf("mask: 1<<2\n");
    print_bin(1<<2);

    //PORTB &= ~(1<<DDB0);
    printf("mask: ~(1<<2)\n");
    print_bin(~(1<<2));


    return 0;
}
