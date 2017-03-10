all: deploy

deploy:
	rsync -avP --exclude '/.git' --exclude '/.gitignore' --filter ':- .gitignore' . orange:~/spotify-connect-client
