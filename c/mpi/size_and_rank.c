#include <stdio.h>
#include <mpi.h>

/*
 * Required packages (Debian): mpi-default-bin, mpi-default-dev
 *
 * mpicc size_and_rank.c -o size_and_rank
 * mpirun -np 4 size_and_rank
 */

int main(int argc, char ** argv)
{
    MPI_Init(&argc, &argv);

    int rank, size;

    MPI_Comm_rank(MPI_COMM_WORLD, &rank); /* get current process id */
    MPI_Comm_size(MPI_COMM_WORLD, &size); /* get number of processes */

    printf("Process %d among %d process in MPI_COMM_WORLD\n", rank, size); 

    MPI_Finalize();
    
    return 0;
}


