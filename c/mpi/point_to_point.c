#include <stdio.h>
#include <mpi.h>

/*
 * Point-to-point ring example.
 *
 * Required packages (Debian): mpi-default-bin, mpi-default-dev
 *
 * Compile:
 *   mpicc point_to_point.c -o point_to_point
 *     or
 *   gcc -o point_to_point -I/usr/include/mpi point_to_point.c -lmpi
 *
 * Run:
 *   mpirun -np 4 point_to_point
 */

int main(int argc, char ** argv)
{
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); /* get current process id */
    MPI_Comm_size(MPI_COMM_WORLD, &size); /* get number of processes */

    int next_rank = (rank+1) % size;
    int previous_rank = (size + rank-1) % size;

    int data_snd = rank + 1000;
    int data_rcv;
    int source = previous_rank;
    int dest = next_rank;
    int tag = 0;
    MPI_Status status;

    if(rank == 0) {

        MPI_Send(&data_snd, 1, MPI_INTEGER, dest, tag, MPI_COMM_WORLD);
        MPI_Recv(&data_rcv, 1, MPI_INTEGER, source, tag, MPI_COMM_WORLD, &status);

    } else {

        MPI_Recv(&data_rcv, 1, MPI_INTEGER, source, tag, MPI_COMM_WORLD, &status);
        MPI_Send(&data_snd, 1, MPI_INTEGER, dest, tag, MPI_COMM_WORLD);
        
    }

    printf("Process %d: received \"%d\" from %d\n", rank, data_rcv, source); 

    MPI_Finalize();
    
    return 0;
}



