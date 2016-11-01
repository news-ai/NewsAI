all:
	git submodule foreach git pull origin master
build:
	rm -rf ../public/blog
	hugo --theme=newsai && mv public ../public/blog
serve:
	hugo server --theme=newsai --buildDrafts --watch