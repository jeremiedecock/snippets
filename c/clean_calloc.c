#include <stdio.h>
#include <stdlib.h>

int main(int argc, char * argv[]) {

    char * pt;

    if( NULL == (pt = calloc( sizeof(*pt), 10 )) ) {
        char * msg = NULL;
        sprintf(msg, "%s %d", __FILE__, __LINE__);

        perror(msg);
        exit(EXIT_FAILURE);
    }

    free(pt);

    exit(EXIT_SUCCESS);

}
