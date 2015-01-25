NAME=article

JDHP_PDF_DIR=~/git/pub/jdhp/files/pdf
#JDHP_HEVEA_DIR=~/git/pub/jdhp/files/hevea
# HEVEA doit être mis dans www plutot que dans download pour les stats et le référencement...
JDHP_HEVEA_DIR=~/git/pub/jdhp/jdhp/hevea
JDHP_UPLOAD_PDF_SCRIPT=~/git/pub/jdhp/files_upload.sh
JDHP_UPLOAD_HEVEA_SCRIPT=~/git/pub/jdhp/jdhp/sync_hevea.sh

#############

all: $(NAME).pdf slides.pdf

.PHONY : all clean init jdhp

## ARTICLE ##

SRCARTICLE=$(NAME).tex\
		   article_packages.tex\
		   commands.tex\
		   setup_package_tikz.tex\
		   setup_package_listings.tex\
		   bibliography.bib

$(NAME).pdf: $(SRCARTICLE)
	pdflatex $(NAME).tex
	bibtex $(NAME)     # this is the name of the .aux file, not the .bib file !
	pdflatex $(NAME).tex
	pdflatex $(NAME).tex

$(NAME).ps: $(SRCARTICLE)
	latex $(NAME).tex
	bibtex $(NAME)     # this is the name of the .aux file, not the .bib file !
	latex $(NAME).tex
	latex $(NAME).tex
	dvips $(NAME).dvi

$(NAME).html: $(SRCARTICLE)
	hevea -fix $(NAME).tex
	bibhva $(NAME)     # this is the name of the .aux file, not the .bib file !
	hevea -fix $(NAME).tex

jdhp:$(NAME).pdf $(NAME).html
	# Copy PDF
	cp -v $(NAME).pdf  $(JDHP_PDF_DIR)/
	# Copy HTML
	@rm -rf $(JDHP_HEVEA_DIR)/$(NAME)
	@mkdir $(JDHP_HEVEA_DIR)/$(NAME)
	cp -v $(NAME).html $(JDHP_HEVEA_DIR)/$(NAME)
	cp -vr fig $(JDHP_HEVEA_DIR)/$(NAME)
	# Sync
	$(JDHP_UPLOAD_PDF_SCRIPT)
	$(JDHP_UPLOAD_HEVEA_SCRIPT)

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
	@rm -f *.haux *.htoc *.hbbl $(NAME).image.tex

init: clean
	@echo "suppression des fichiers cibles"
	@rm -f *.pdf
	@rm -f *.ps
	@rm -f $(NAME).html
