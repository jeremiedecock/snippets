all: slides.pdf

## SLIDES ##

SRCSLIDES=slides_packages.tex\
		  commands.tex\
		  bibliography.bib\
		  setup_package_tikz.tex\
		  setup_package_listings.tex\
		  slides_main.tex\
		  slides_section_*.tex\
		  slides_appendix.tex\
#SRCTIKZ=

slides.pdf: $(SRCSLIDES) $(SRCTIKZ) slides.tex
	pdflatex slides.tex
	bibtex slides     # this is the name of the .aux file, not the .bib file !
	pdflatex slides.tex
	pdflatex slides.tex

slides_handout.pdf: $(SRCSLIDES) $(SRCTIKZ) slides_handout.tex
	pdflatex slides_handout.tex
	#bibtex slides_handout     # this is the name of the .aux file, not the .bib file !
	#pdflatex slides_handout.tex
	pdflatex slides_handout.tex

slides_notes.pdf: $(SRCSLIDES) $(SRCTIKZ) slides_notes.tex
	pdflatex slides_notes.tex
	#bibtex slides_notes     # this is the name of the .aux file, not the .bib file !
	#pdflatex slides_notes.tex
	pdflatex slides_notes.tex


## CLEAN ##

clean:
	@echo "suppression des fichiers de compilation"
	@rm -f *.log *.aux *.dvi *.toc *.lot *.lof *.out *.nav *.snm *.bbl *.blg *.vrb

init: clean
	@echo "suppression des fichiers cibles"
	@rm -f *.pdf
	@rm -f *.ps
