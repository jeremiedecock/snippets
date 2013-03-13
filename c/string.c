/* 
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc string.c
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

////////

int main(int argc, char * argv[])
{
    // strcat ///////////////

    printf("\n*** strcat ***\n");
    {
        char str[20] = "Hello";
        strcat(str, " world!");
        printf("%s\n", str);
    }
    
    // strcat (return) //////
    
    printf("\n*** strcat (return) ***\n");
    {
        char str[20] = "Hello";
        printf("%s\n", strcat(str, " world!"));
    }
    
    // strlen ///////////////

    printf("\n*** strlen ***\n");
    {
        char str[20] = "Hello";
        printf("%d\n", strlen(str));
    }
    
    // strcpy ///////////////

    printf("\n*** strcpy ***\n");
    {
        //char * str;  // ERROR! pending pointer
        //char * str = malloc(10);
        char str[10];
        strcpy(str, "Hello");

        printf("%s\n", str);
    }
    
    // strcpy (return) //////

    printf("\n*** strcpy (return) ***\n");
    {
        char str[10];
        printf("%s\n", strcpy(str, "Hello"));
    }
    
    // strcmp //////

    printf("\n*** strcmp ***\n");
    {
        char str[] = "Hello";
        printf("%d\n", strcmp(str, "Hello"));
    }
    
    // TODO: secure functions: strncpy, ... //////
    
    // TODO: atoi, sprintf, sscanf, ... //////
    
    // TODO: wchar functions... //////

    exit(EXIT_SUCCESS);
}

