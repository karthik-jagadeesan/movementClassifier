# Make file for Python is just a bunch of PHONY commands

.PHONY : all
all : test
	python3 app

.PHONY : clean
clean :
	cd app/
	cd __pycache__
	rm rf *
	cd ..
	rmdir __pycache__

.PHONY : test
test: setPath

.PHONY : setPath
setPath:
	export PYTHONPATH=.:$(CURDIR)
