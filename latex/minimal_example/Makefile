NAME=article

#############

all: $(NAME).pdf

.PHONY : all clean init jdhp

## ARTICLE ##

SRCARTICLE=$(NAME).tex

$(NAME).pdf: $(SRCARTICLE)
	pdflatex $(NAME).tex
	pdflatex $(NAME).tex

$(NAME).ps: $(SRCARTICLE)
	latex $(NAME).tex
	latex $(NAME).tex
	dvips $(NAME).dvi

$(NAME).html: $(SRCARTICLE)
	hevea -fix $(NAME).tex
	hevea -fix $(NAME).tex

## CLEAN ##

clean:
	@echo "suppression des fichiers de compilation"
	@rm -f *.log *.aux *.dvi *.toc *.lot *.lof *.out *.nav *.snm *.bbl *.blg *.vrb
	@rm -f *.haux *.htoc *.hbbl $(NAME).image.tex

init: clean
	@echo "suppression des fichiers cibles"
	@rm -f $(NAME).pdf
	@rm -f $(NAME).ps
	@rm -f $(NAME).html
