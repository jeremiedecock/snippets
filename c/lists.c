#include <stdlib.h>
#include <stdio.h>

typedef struct list {
    int data;
    struct list * next;
} list;

list * make_elem(void) {
    list * pe;

    if(NULL == (pe = malloc(sizeof(list)))) {
        fprintf(stderr, "Erreur d'allocation memoire\n");
        exit(EXIT_FAILURE);
    }

    return pe;
}

int main() {

    list *pl, *pe1, *pe2, *pe3, *pe4;

    pe1 = make_elem();
    pe2 = make_elem();
    pe3 = make_elem();
    pe4 = make_elem();

    pe1->data = 2;
    pe2->data = 3;
    pe3->data = 5;
    pe4->data = 7;

    pl = pe1;

    pe1->next = pe2;
    pe2->next = pe3;
    pe3->next = pe4;
    pe4->next = NULL;

    list * c;

    for(c=pl ; c ; c=c->next) {
        printf("%d\n", c->data);
    }

    free(pe1);
    free(pe2);
    free(pe3);
    free(pe4);

    return 0;
}
