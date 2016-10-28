all:
	git submodule foreach git pull origin master
build:
	hugo --theme=newsai
serve:
	hugo server --theme=newsai --buildDrafts --watch