CC = gcc

CFLAGS = 
LIBS = -lgsl -lgslcblas -lm

.PHONY : all clean init

all : blas_gsl_matrix blas_gsl_vector blas_gsl_matrix_view

blas_gsl_matrix : blas_gsl_matrix.c
	$(CC) -o $@ $(CFLAGS) $< $(LIBS)

blas_gsl_vector : blas_gsl_vector.c
	$(CC) -o $@ $(CFLAGS) $< $(LIBS)

blas_gsl_matrix_view : blas_gsl_matrix_view.c
	$(CC) -o $@ $(CFLAGS) $< $(LIBS)

clean :
	rm blas_gsl_matrix blas_gsl_vector blas_gsl_matrix_view 2> /dev/null

init : clean

