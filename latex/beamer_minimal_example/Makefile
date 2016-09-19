NAME=slides

#############

all: $(NAME).pdf

.PHONY : all clean init

## SLIDES ##

SRCSLIDES=$(NAME).tex

$(NAME).pdf: $(SRCSLIDES) $(NAME).tex
	pdflatex $(NAME).tex
	pdflatex $(NAME).tex

## CLEAN ##

clean:
	@echo "suppression des fichiers de compilation"
	@rm -f *.log *.aux *.dvi *.toc *.lot *.lof *.out *.nav *.snm *.bbl *.blg *.vrb

init: clean
	@echo "suppression des fichiers cibles"
	@rm -f $(NAME).pdf
