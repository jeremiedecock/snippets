CC = g++

CFLAGS = 

.PHONY : all clean init

all : chrono time_budget_loop timer time_string_conversion

chrono : chrono.cc
	$(CC) -o $@ $(CFLAGS) $<

time_budget_loop : time_budget_loop.cc
	$(CC) -o $@ $(CFLAGS) $<

timer : timer.cc
	$(CC) -o $@ $(CFLAGS) $<

time_string_conversion : time_string_conversion.cc
	$(CC) -o $@ $(CFLAGS) $< -lboost_date_time

clean :
	rm chrono time_budget_loop timer time_string_conversion 2> /dev/null

init : clean

