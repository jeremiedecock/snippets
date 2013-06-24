#include <stdio.h>
#include <mpi.h>

/*
 * Broadcast example.
 *
 * Required packages (Debian): mpi-default-bin, mpi-default-dev
 *
 * Compile:
 *   mpicc broadcast.c -o broadcast
 *     or
 *   gcc -o broadcast -I/usr/include/mpi broadcast.c -lmpi
 *
 * Run:
 *   mpirun -np 4 broadcast
 */

int main(int argc, char ** argv)
{
    MPI_Init(&argc, &argv);

    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); /* get current process id */

    int data = 1000;

    if(rank == 0) {
        MPI_Bcast(&data, 1, MPI_INTEGER, rank, MPI_COMM_WORLD);
    }

    printf("Process %d: received \"%d\" from 0\n", rank, data); 

    MPI_Finalize();
    
    return 0;
}



