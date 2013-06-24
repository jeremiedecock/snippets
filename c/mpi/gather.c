#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

/*
 * Gather example.
 *
 * Required packages (Debian): mpi-default-bin, mpi-default-dev
 *
 * Compile:
 *   mpicc gather.c -o gather
 *     or
 *   gcc -o gather -I/usr/include/mpi gather.c -lmpi
 *
 * Run:
 *   mpirun -np 4 gather
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

    int send_buffer[2];
    int * recv_buffer = NULL;

    int send_count = 2;      // the number of elements that are sent by each process to root
    int recv_count = 0;      // the number of elements that are stored in the recvbuffer

    int root = 0;            // the rank of the root process who is responsible for performing MPI_scatter function

    int i;
    for(i=0 ; i<2 ; i++) {
        send_buffer[i] = rank * 1000 + i;
    }

    // only the root process allocates memory for recv_buffer
    if(rank == root) {
        recv_count = 2 * size;
        recv_buffer = (int *) malloc(recv_count * sizeof(int));
    }

    MPI_Gather(send_buffer, 2, MPI_INTEGER, recv_buffer, 2, MPI_INTEGER, root, MPI_COMM_WORLD);

    if(rank == root) {
        for(i=0 ; i<recv_count ; i++) {
            printf("recv_buffer[%d] = %d\n", i, recv_buffer[i]);
        }
    }

    if(rank == root) {
        free(recv_buffer);
    }

    MPI_Finalize();
    
    return 0;
}



