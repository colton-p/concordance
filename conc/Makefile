#TGT=taylor
TGT=$(MAKECMDGOALS)

.PHONY: $(TGT)
	echo $(TGT)

$(TGT): data/conc/$(TGT).json
	echo $(TGT)

data/conc/$(TGT).json: data/tokenized/$(TGT).json concord.py
	python3 concord.py $(TGT) --infile $< --outfile $@

data/tokenized/$(TGT).json: data/clean_lyrics/$(TGT).json tokens.py
	python3 tokens.py $(TGT) --infile $< --outfile $@

data/clean_lyrics/$(TGT).json: data/raw_lyrics/$(TGT).json clean.py
	python3 clean.py $(TGT) --infile $< --outfile $@

data/raw_lyrics/$(TGT).json: extract.py
	python3 extract.py $(TGT) --outfile $@


#
#data/clean_lyrics/taylor.json: data/raw_lyrics/taylor.json
#	echo 'hi'
#

#TGT=$(MAKECMDGOALS)
#
#SRC=src
#TMP=tmp
#IMG=doc/img
#
#.PHONY: $(TGT)

# $(TGT): $(IMG)/$(TGT).png

# $(IMG)/$(TGT).png: $(TMP)/$(TGT).eps
# 	convert -density 300 $< $@
# $(TMP)/$(TGT).eps: $(TMP)/$(TGT).pdf
# 	pdftops -eps $<
# $(TMP)/$(TGT).pdf: $(SRC)/$(TGT).tex
# 	pdflatex -output-directory $(TMP) $<

# clean:
# 	rm $(TMP)/*
