.PHONY: all clean

all: arxiv_preprint.pdf

arxiv_preprint.pdf: arxiv_preprint.tex references.bib
	pdflatex arxiv_preprint.tex
	bibtex arxiv_preprint
	pdflatex arxiv_preprint.tex
	pdflatex arxiv_preprint.tex

clean:
	rm -f *.aux *.log *.bbl *.blg *.out *.pdf
