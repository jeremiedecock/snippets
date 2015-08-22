NAME=index

# rst2html options ############################################################

# See man rst2html for more information

TITLE="Documenter un projet Python"

#LANGUAGE=en
LANGUAGE=fr

MATH_OUTPUT="MathJax"

SOURCE_URL="https://github.com/jeremiedecock"

###############################################################################

all: $(NAME).html $(NAME)_slides.html

.PHONY : all clean init

SRCFILES=$(wildcard *.rst) Makefile

## ARTICLE ##

$(NAME).html: $(SRCFILES)
	rst2html --title=$(TITLE) --date --time --generator \
		--language=$(LANGUAGE) --tab-width=4 --math-output=$(MATH_OUTPUT) \
		--source-url=$(SOURCE_URL) \
		$(NAME).rst $@

## SLIDES ##

$(NAME)_slides.html: $(SRCFILES)
	rst2s5 --title=$(TITLE) --date --time --generator \
		--language=$(LANGUAGE) --tab-width=4 --math-output=$(MATH_OUTPUT) \
		--source-url=$(SOURCE_URL) \
		$(NAME).rst $@

## CLEAN ##

clean:
	@rm -rvf $(NAME).html $(NAME)_slides.html ui/

init: clean
