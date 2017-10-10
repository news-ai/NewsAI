all:
	git submodule foreach git pull origin master
build:
	rm -rf ../public/pitchbook
	hugo
	mv public ../public/pitchbook
serve:
	hugo server --buildDrafts --watch