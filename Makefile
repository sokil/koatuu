.PHONY: build docker

build:
	find . -maxdepth 1 -type f -name "*.csv" | xargs -I{} python convert.py --source {}

docker-run:
	docker run --name="koatuu" --rm -it -v `pwd`:/docker-entrypoint-initdb.d -e MYSQL_ALLOW_EMPTY_PASSWORD=yes -e MYSQL_DATABASE=test mariadb

docker-cli:
	docker exec -it koatuu mysql --default-character-set="UTF8" test

docker-stop:
	docker stop koatuu
