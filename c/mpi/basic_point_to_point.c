#include <stdio.h>
#include <mpi.h>

/*
 * Required packages (Debian): mpi-default-bin, mpi-default-dev
 *
 * Compile:
 *   mpicc basic_point_to_point.c -o basic_point_to_point
 *     or
 *   gcc -o basic_point_to_point -I/usr/include/mpi basic_point_to_point.c -lmpi
 *
 * Run:
 *   mpirun -np 4 basic_point_to_point
 */

int main(int argc, char ** argv)
{
    MPI_Init(&argc, &argv);

    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); /* get current process id */

    if(rank == 0) {

        // 1st process -> send a message to the 4th process
        int data = 123;
        int tag = 0;
        int dest = 3;

        printf("Process %d: sending a message to %d\n", rank, dest); 
        MPI_Send(&data, 1, MPI_INTEGER, dest, tag, MPI_COMM_WORLD);

    } else if(rank == 3) {

        // 4th process -> receive a message from the 1st process
        int data;
        int source = 0;
        int tag = 0;
        MPI_Status status;

        printf("Process %d: waiting a message from %d\n", rank, source); 
        MPI_Recv(&data, 1, MPI_INTEGER, source, tag, MPI_COMM_WORLD, &status);
        printf("Process %d: received \"%d\" from %d\n", rank, data, source); 
        
    } else {
        printf("Process %d: nothing to do... bye\n", rank); 
    }

    MPI_Finalize();
    
    return 0;
}


