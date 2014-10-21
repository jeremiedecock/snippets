all: article.pdf

## ARTICLE ##

SRCARTICLE=article.tex\
		   article_packages.tex\
		   commands.tex\
		   setup_package_tikz.tex\
		   setup_package_listings.tex\
		   bibliography.bib

article.pdf: $(SRCARTICLE)
	pdflatex article.tex
	bibtex article     # this is the name of the .aux file, not the .bib file !
	pdflatex article.tex
	pdflatex article.tex

article.ps: $(SRCARTICLE)
	latex article.tex
	bibtex article     # this is the name of the .aux file, not the .bib file !
	latex article.tex
	latex article.tex
	dvips article.dvi

## CLEAN ##

clean:
	@echo "suppression des fichiers de compilation"
	@rm -f *.log *.aux *.dvi *.toc *.lot *.lof *.out *.nav *.snm *.bbl *.blg *.vrb

init: clean
	@echo "suppression des fichiers cibles"
	@rm -f *.pdf
	@rm -f *.ps
