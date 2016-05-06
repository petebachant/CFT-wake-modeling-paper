
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
