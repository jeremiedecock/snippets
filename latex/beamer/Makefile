all: slides.pdf

SRCSLIDES=slides.tex

slides.pdf: $(SRCSLIDES) slides.tex
	pdflatex slides.tex
	pdflatex slides.tex

## CLEAN ##

clean:
	@echo "suppression des fichiers de compilation"
	@rm -f *.log *.aux *.dvi *.toc *.lot *.lof *.out *.nav *.snm *.bbl *.blg *.vrb

init: clean
	@echo "suppression des fichiers cibles"
	@rm -f *.pdf
	@rm -f *.ps
