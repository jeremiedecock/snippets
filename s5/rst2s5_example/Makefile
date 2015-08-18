NAME=slides

############

all: $(NAME).html

.PHONY : all clean init

## SLIDES ##

SRCFILES=$(NAME).rst

$(NAME).html: $(SRCFILES)
	rst2s5 $(NAME).rst $(NAME).html

## CLEAN ##

clean:
	@rm -rvf ui $(NAME).html

init: clean
	@rm -rvf ui $(NAME).html
