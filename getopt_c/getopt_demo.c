#include <stdio.h>
#include <getopt.h>

int main(int argc, char * argv[]) {
    
    int c;
    while(1) {
        static struct option long_options[] =
        {
            {"version", no_argument,       0, 'v'},
            {"opt1",    required_argument, 0, 'o'},
            {0, 0, 0, 0}
        };

        /* getopt_long stores the option index here */
        int option_index = 0;

        c = getopt_long(argc, argv, "va:", long_options, &option_index);

        /* detect the end of the options */
        if(c == -1)
            break;

        switch(c) {
            case 'v' : printf("set v option\n");
                       break;
            case 'a' : printf("set a option = %s\n", optarg);
                       break;
            case '?' : printf("error");
        }
    }

    /* get any remaining command line arguments (not options) */
    while(optind < argc)
        printf("%s\n", argv[optind++]);

    return 0;
}
