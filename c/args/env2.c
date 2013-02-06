#include <stdlib.h>
#include <stdio.h>

int main(int argc, char * argv[], char * envp[])
{
    // PRINT ALL VAR
    int i;
    for(i=0 ; envp[i] != NULL ; i++) {
        printf("%s\n", envp[i]);
    }
    
    // UPDATE AND PRINT PATH VALUE
    printf("\nPATH=%s\n\n", getenv("PATH"));
    putenv("PATH=/usr/bin");
    printf("PATH=%s\n", getenv("PATH"));

    return 0;
}
