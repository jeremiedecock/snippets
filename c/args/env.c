#include <stdlib.h>
#include <stdio.h>

int main(int argc, char * argv[], char * envp[])
{
    // PRINT ALL VAR
    int i = 0;
    while(envp[i] != NULL) {
        printf("%s\n", envp[i]);
        i++;
    }
    
    // UPDATE AND PRINT PATH VALUE
    printf("\nPATH=%s\n\n", getenv("PATH"));
    putenv("PATH=/usr/bin");
    printf("PATH=%s\n", getenv("PATH"));

    return 0;
}
