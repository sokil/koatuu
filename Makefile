.PHONY: build docker

build:
	find . -maxdepth 1 -type f -name "*.csv" | xargs -I{} python convert.py --csv {}

docker:
	docker run --rm -it -v `pwd`:/docker-entrypoint-initdb.d -e MYSQL_ROOT_PASSWORD=test -e MYSQL_DATABASE=test mariadb
