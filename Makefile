FILES_IPYNB=$(sort $(wildcard L??/*.ipynb) $(wildcard L??/*/*.ipynb))
FILES_PY=$(sort $(wildcard libitmal/*.py))
FILES_WEB=$(sort $(wildcard Html/*.html))

CHECK_FOR_TEXT=grep "$1" $(FILES_IPYNB) -R || echo "  OK, no '$1'.."

.PHONY:all
all:
	@ echo "Doing nothing!"
	@ echo "  This makefile just for parsing and checking,"
	@ echo "  enjoy .c"

.PHONY:check
check:
	@ echo "CHECKING (for various no-no's in .ipynb files).."
	@ echo "  FILES: $(FILES_IPYNB)"
	@ $(call CHECK_FOR_TEXT,itundervisining) 
	@ $(call CHECK_FOR_TEXT,BB-Cou-UUVA) 
	@ $(call CHECK_FOR_TEXT,blackboard.au.dk) 
	@ $(call CHECK_FOR_TEXT,blackboard) 
	@ $(call CHECK_FOR_TEXT,Blackboard) 
	@ $(call CHECK_FOR_TEXT,dk/GITMAL/)
	@ $(call CHECK_FOR_TEXT,27524)# E21
	@ $(call CHECK_FOR_TEXT,53939)# F22
	@ $(call CHECK_FOR_TEXT,70628)# E22
	@ $(call CHECK_FOR_TEXT,91157)# F23
	@ $(call CHECK_FOR_TEXT,91157)# F23
	@# $(call CHECK_FOR_TEXT,mbox)
	@ echo "DONE: all ok"

.PHONY:checkpages
checkpages:
	@ echo "CHECKING (for pages).."
	@ egrep --color "p\.\[\ ]+" $(FILES_WEB) $(FILES_IPYNB) || true
	@ egrep --color "[ ][p]+[ ]+[0-9]+" $(FILES_WEB) $(FILES_IPYNB) || true
	@ egrep --color "[ ][p]+[0-9]+" $(FILES_WEB) $(FILES_IPYNB) || true
	@ echo "WEBPAGES.."
	@ egrep --color "p\.[0-9]+" $(FILES_WEB) 
	@ echo "IPYNB FILES.."
	@ egrep --color "p\.[0-9]+" $(FILES_IPYNB)

.PHONY:test
test:
	@#for var in $(FILES_PY); do echo $$var $@; done
	@#libitmal/dataloaders.py
	libitmal/kernelfuns.py
	libitmal/utils.py
	libitmal/versions.py

.PHONY:pull
pull:
	@ echo "PULL" | tee -a log_pull.txt
	@ date        | tee -a log_pull.txt
	@ git pull 2>>log_pull.err | tee -a log_pull.txt

#PARSED=$(foreach f,$(FILES_IPYNB),$(shell (python -m json.tool $(f) 1>/dev/null 2>/dev/null && echo >&2 "OK $(f)")|| (echo >&2 $(f) && python -m json.tool $(f))))
#.PHONY:parsecheck
#parsecheck:
#	@#echo PARSE_ERRORS=$(PARSED)
#	@#cat $(PARSED) | tr ' ' '\n' # |  xargs -I % sh -c 'echo %;'

.PHONY:clean
clean:
	@ find . -iname ".ipynb_checkpoints" -exec rm -r {} \;
