pdf: slides.md
	pandoc -t beamer slides.md -o slides.pdf \
	-V theme=Goettingen \
	--metadata-file=config-slides.yaml \
	--metadata date="`date +'%d %B %Y'`" \
	--slide-level=2 \
	--citeproc \
	--csl=bib/acm-sig-proceedings-long-author-list.csl \
	--bibliography=bib/project.bib \
