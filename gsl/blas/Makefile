CC = gcc

CFLAGS = 
LIBS = -lgsl -lgslcblas -lm

.PHONY : all clean init

all : gsl_blas_dgemm gsl_blas_dgemv gsl_blas_ddot gsl_blas_dgemm_matrix_view

gsl_blas_dgemm : gsl_blas_dgemm.c
	$(CC) -o $@ $(CFLAGS) $< $(LIBS)

gsl_blas_dgemv : gsl_blas_dgemv.c
	$(CC) -o $@ $(CFLAGS) $< $(LIBS)

gsl_blas_ddot : gsl_blas_ddot.c
	$(CC) -o $@ $(CFLAGS) $< $(LIBS)

gsl_blas_dgemm_matrix_view : gsl_blas_dgemm_matrix_view.c
	$(CC) -o $@ $(CFLAGS) $< $(LIBS)

clean :
	rm gsl_blas_dgemm gsl_blas_dgemv gsl_blas_ddot gsl_blas_dgemm_matrix_view 2> /dev/null

init : clean

