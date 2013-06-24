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
 *
 * See:
 *   http://www.mpiprogramming.com/mpi/
 */

int main(int argc, char ** argv)
{
    MPI_Init(&argc, &argv);

    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); /* get current process id */

    int buffer[10];
    int root = 0;

    if(rank == root) {
        int i;
        for(i=0 ; i<10 ; i++)
            buffer[i] = i*2;
    }

    MPI_Bcast(buffer, 10, MPI_INT, root, MPI_COMM_WORLD);

    if(rank!=0){
        int i;
        for(i=0 ; i<10 ; i++) {
            printf("Process %d: buffer[%d]=%d\n", rank, i, buffer[i]);
        }
    }

    MPI_Finalize();
    
    return 0;
}



