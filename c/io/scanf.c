/* 
 * Scanf
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc scanf.c
 * See "man 3 scanf" for more info
 *
 */

#include <stdio.h>

int main(int argc, char * argv[])
{
    int n1, n2;

    printf("Enter one number: ");
    scanf("%d", &n1);
    printf("n1=%d\n", n1);

    printf("Enter two numbers: ");
    scanf("%d%d", &n1, &n2);
    printf("n1=%d\nn2=%d\n", n1, n2);

    return 0;
}
