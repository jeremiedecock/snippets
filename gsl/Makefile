CC = gcc

CFLAGS = 
LIBS = -lgsl -lgslcblas -lm

.PHONY : all clean init

all : gsl_fcmp gsl_vector identity_matrix

gsl_fcmp : gsl_fcmp.c
	$(CC) -o $@ $(CFLAGS) $< $(LIBS)

gsl_vector : gsl_vector.c
	$(CC) -o $@ $(CFLAGS) $< $(LIBS)

identity_matrix : identity_matrix.c
	$(CC) -o $@ $(CFLAGS) $< $(LIBS)

clean :
	rm gsl_fcmp gsl_vector identity_matrix 2> /dev/null

init : clean

