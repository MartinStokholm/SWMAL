DOC=demo
EXTERNALS=$(wildcard *.sty) $(wildcard Figs/*) Makefile

$(DOC).pdf: $(DOC).tex

%.pdf: %.tex $(EXTERNALS)
	pdflatex -interaction=nonstopmode $< || true
	@# echo -n $(PURPLE)"rubber-info " $(<:tex=log) $(GREEN)	
	@# - rubber-info $(<:tex=log)
	@# echo $(NC)	
	@# rm current.pdf 2>/dev/null || true
	@# ln -s $@ current.pdf 
	@# (grep "Rerun to get outlines right" $(<:tex=log) && echo "**RERUN**" && touch $< && $(MAKE) -s $(MAKEARGS) $@) || true

.PHONY: edit
edit:
	joe demo.tex

.PHONY: cleanfigs
cleanfigs:
	@ - rm -r $(DIAEPS) Figs/*-eps-converted-to.pdf 

.PHONY: clean
clean:
	@ - rm -f $(DOC).pdf current.pdf out.txt *.vrb *.nav *.out *.snm *.log *.dvi *.aux *.toc *.idx *.ilg *.ind *.bbl *.blg *.backup *.bak $(EXTRA_CLEAN)
