NAME=article

JDHP_PDF_DIR=~/git/pub/jdhp/files/pdf
JDHP_HEVEA_DIR=~/git/pub/jdhp/files/hevea
JDHP_UPLOAD_SCRIPT=~/git/pub/jdhp/files_upload.sh

#############

all: $(NAME).pdf

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
	$(JDHP_UPLOAD_SCRIPT)

## CLEAN ##

clean:
	@echo "suppression des fichiers de compilation"
	@rm -f *.log *.aux *.dvi *.toc *.lot *.lof *.out *.nav *.snm *.bbl *.blg *.vrb
	@rm -f *.haux *.htoc $(NAME).image.tex

init: clean
	@echo "suppression des fichiers cibles"
	@rm -f $(NAME).pdf
	@rm -f $(NAME).ps
	@rm -f $(NAME).html
