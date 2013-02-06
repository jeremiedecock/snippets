#include <stdlib.h>
#include <stdio.h>

extern char ** environ;

int main(int argc, char * argv[])
{
    // PRINT ALL VAR
    int i;
    for(i=0 ; environ[i] != NULL ; i++) {
        printf("%s\n", environ[i]);
    }
    
    // UPDATE AND PRINT PATH VALUE
    printf("\nPATH=%s\n\n", getenv("PATH"));
    putenv("PATH=/usr/bin");
    printf("PATH=%s\n", getenv("PATH"));

    return 0;
}
