/* 
 * Uname: display system information like "uname -a" unix command
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc uname.c
 * See "man 2 uname" for more info
 *
 */

#include <stdio.h>
#include <string.h>

#ifdef __unix__
#include <sys/utsname.h>
#endif

// Return system informations in a string
char * get_sysinfo(void)
{
    static char str[2048] = "unknown";  // TODO: assume a max size... (bad) [see utsname.h]

#ifdef __unix__
    struct utsname buf;
    int result = uname(&buf);

    if(result == 0) {
        strcpy(str, buf.sysname);
        strcat(str, " ");
        strcat(str, buf.nodename);
        strcat(str, " ");
        strcat(str, buf.release);
        strcat(str, " ");
        strcat(str, buf.version);
        strcat(str, " ");
        strcat(str, buf.machine);
        strcat(str, " ");
    }
#endif

    return str;
}

int main(int argc, char * argv[])
{
    fprintf(stdout, "%s\n", get_sysinfo());

    return 0;
}

