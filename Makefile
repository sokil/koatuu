default: build clean

download:
	mkdir -p ./build
	wget http://www.ukrstat.gov.ua/klasf/st_kls/koatuu.zip -O ./build/koatuu.zip
	unzip -o ./build/koatuu.zip -d ./build/

build: build-mysql build-postgres

build-mysql: download
	find ./build -maxdepth 1 -type f -name "KOATUU_*.xls" | xargs -I{} python convert.py --source {} --format mysql --target KOATUU.mysql.sql

build-postgres: download
	find ./build -maxdepth 1 -type f -name "KOATUU_*.xls" | xargs -I{} python convert.py --source {} --format postgres --target KOATUU.postgres.sql

build-opendata835: download
	find ./build -maxdepth 1 -type f -name "KOATUU_*.xls" | xargs -I{} python convert.py --source {} --format opendata835 --target KOATUU.opendata835.sql

clean:
	rm -rf build

docker-run:
	docker run --name="koatuu" --rm -it -v `pwd`:/docker-entrypoint-initdb.d -e MYSQL_ALLOW_EMPTY_PASSWORD=yes -e MYSQL_DATABASE=test mariadb

docker-cli:
	docker exec -it koatuu mysql --default-character-set="UTF8" test

docker-stop:
	docker stop koatuu
