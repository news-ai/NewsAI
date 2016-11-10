all:
	git submodule foreach git pull origin master
build:
	rm -rf ../public/blog
	hugo && mv public ../public/blog
serve:
	hugo server --buildDrafts --watch