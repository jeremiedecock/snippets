#include <stdio.h>
#include <mpi.h>

/*
 * Required packages (Debian): mpi-default-bin, mpi-default-dev
 *
 * Compile:
 *   mpicc hello.c -o hello
 *     or
 *   gcc -o hello -I/usr/include/mpi hello.c -lmpi
 *
 * Run:
 *   mpirun -np 4 hello
 */

int main(int argc, char ** argv)
{
    int ierr; 

    ierr = MPI_Init(&argc, &argv);
    printf("Hello world\n"); 
    ierr = MPI_Finalize();
    
    return ierr;
}

