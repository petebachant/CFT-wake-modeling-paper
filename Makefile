
.PHONY: paper
paper:
	latexmk -pdf paper.tex


.PHONY: cover-letter
cover-letter:
	cd cover-letter
	pandoc --template=template-letter.tex cover-letter.md -o cover-letter.pdf


.PHONY: view
view: paper
ifeq ($(shell uname -s),MINGW64_NT-10.0)
	start "" paper.pdf
else
	echo "Viewing only setup for Windows"
endif


.PHONY: clean
clean:
	latexmk -c paper.tex


.PHONY: zip
zip:
	python scripts/zip.py


## bib:             Update BibTeX database
.PHONY: bib
bib:
	python scripts/getbib.py


## word-count:      Count words in PDF
.PHONY: word-count
word-count:
	@pdftotext paper.pdf
	@wc -w paper.txt
	@rm paper.txt


## reviews:         Build PDFs of review responses
.PHONY: reviews
reviews: reviews/reviewer2-response.md reviews/reviewer3-response.md
	pandoc reviews/reviewer2-response.md -o reviews/reviewer2-response.pdf -H reviews/quote-config.tex
	pandoc reviews/reviewer3-response.md -o reviews/reviewer3-response.pdf -H reviews/quote-config.tex


.PHONY: help
help: Makefile
	@sed -n "s/^##//p" $<
