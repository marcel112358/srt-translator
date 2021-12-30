# INPUTPATH without the trailing slash (eg. /home/user/Videos/subtitles)
INPUTPATH=subtitles
SRC_LANG=sv
SRC_FORMAT=vtt
DEST_LANG=de
DEST_FORMAT=vtt
API_KEY=

.PHONY: all
all: $(subst .$(SRC_LANG).$(SRC_FORMAT),.$(DEST_LANG).$(DEST_FORMAT),$(wildcard $(INPUTPATH)/*.$(SRC_LANG).$(SRC_FORMAT)))

# TODO: does not work for DEST_FORMAT == srt?!
ifneq ($(DEST_FORMAT), "srt")
%.$(DEST_LANG).$(DEST_FORMAT): %.$(DEST_LANG).srt
	ffmpeg -i $< $@
endif

ifneq ($(SRC_FORMAT), "srt")
%.$(SRC_LANG).srt: %.$(SRC_LANG).$(SRC_FORMAT)
	ffmpeg -i $< $@
endif

%.$(DEST_LANG).srt: | srt-translator/__init__.py %.$(SRC_LANG).srt
	python3 $(word 1,$|) -i $(word 2,$|) -o $@ --src-lang $(SRC_LANG) --dest-lang $(DEST_LANG) --api-key $(API_KEY)

toUnderscore:
	rename "s/ /_/g" $(INPUTPATH)/*

toSpace:
	rename "s/_/ /g" $(INPUTPATH)/*

clean:
	$(RM) $(INPUTPATH)/*.$(DEST_LANG)*