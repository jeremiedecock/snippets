CC = g++

# Boost::datetime don't requires to link a library
CFLAGS = 
LIBS = 

.PHONY : all clean init

all : chrono time_budget_loop timer

chrono : chrono.cc
	$(CC) -o $@ $(CFLAGS) $(LIBS) $<

time_budget_loop : time_budget_loop.cc
	$(CC) -o $@ $(CFLAGS) $(LIBS) $<

timer : timer.cc
	$(CC) -o $@ $(CFLAGS) $(LIBS) $<

clean :
	rm chrono time_budget_loop timer 2> /dev/null

init : clean

