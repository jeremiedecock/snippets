#include <stdio.h>
#include <unistd.h>

int global_var = 3;

int main(void)
{
    int local_var = 3;

    pid_t proc_id = fork();

    if(proc_id == 0) {        // Child process

        global_var++;
        local_var++;

        fprintf(stdout, "Child:  global_var=%d local_var=%d\n", global_var, local_var);

    } else {                  // Parent process

        global_var--;
        local_var--;

        fprintf(stdout, "Parent: global_var=%d local_var=%d\n", global_var, local_var);

    }
}
