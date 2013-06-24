#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

/*
 * Scatter example.
 *
 * Required packages (Debian): mpi-default-bin, mpi-default-dev
 *
 * Compile:
 *   mpicc scatter.c -o scatter
 *     or
 *   gcc -o scatter -I/usr/include/mpi scatter.c -lmpi
 *
 * Run:
 *   mpirun -np 4 scatter
 *
 * See:
 *   http://www.mpiprogramming.com/mpi/
 */

int main(int argc, char ** argv)
{
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); /* get current process id */
    MPI_Comm_size(MPI_COMM_WORLD, &size); /* get number of processes */

    int * send_buffer = NULL;
    int recv_buffer[2];

    int send_count = 2;      // the number of elements that are sent to each process
    int recv_count = 2;      // the number of elements that are stored in the recvbuffer

    int root = 0;            // the rank of the root process who is responsible for performing MPI_scatter function

    // only the root process allocates memory for send_buffer
    if(rank == root) {
        int data_size = size * send_count;
        send_buffer = (int*) malloc(data_size * sizeof(int));

        int i;
        for(i=0 ; i<data_size ; i++)
            send_buffer[i] = 2*i;
    }

    MPI_Scatter(send_buffer, send_count, MPI_INTEGER, &recv_buffer, recv_count, MPI_INTEGER, root, MPI_COMM_WORLD);

    printf("Process %d: received \"[%d,%d]\" from %d\n", rank, recv_buffer[0], recv_buffer[1], root); 

    if(rank == root) {
        free(send_buffer);
    }

    MPI_Finalize();
    
    return 0;
}



