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

docker-mysql-run:
	docker run --name="koatuu_mysql" --rm -it -v `pwd`:/docker-entrypoint-initdb.d -e MYSQL_ALLOW_EMPTY_PASSWORD=yes -e MYSQL_DATABASE=test mariadb

docker-mysql-cli:
	docker exec -it koatuu_mysql mysql --default-character-set="UTF8" test

docker-mysql-stop:
	docker stop koatuu_mysql

docker-postgres-run:
	docker run --name="koatuu_postgres" --rm -d -it -e POSTGRES_DB=test -e POSTGRES_PASSWORD=pg -e POSTGRES_USER=pg postgres
	docker cp KOATUU.postgres.sql koatuu_postgres:/docker-entrypoint-initdb.d/KOATUU.postgres.sql
	docker exec -it koatuu_postgres psql -Upg -dtest -f /docker-entrypoint-initdb.d/KOATUU.postgres.sql

docker-postgres-cli:
	docker exec -it koatuu_postgres psql -Upg test

docker-postgres-stop:
	docker stop koatuu_postgres

docker-opendata835-run:
	docker run --name="koatuu_opendata835" --rm -d -it -e POSTGRES_DB=test -e POSTGRES_PASSWORD=pg -e POSTGRES_USER=pg postgres
	docker cp KOATUU.opendata835.sql koatuu_opendata835:/docker-entrypoint-initdb.d/KOATUU.opendata835.sql
	docker exec -it koatuu_opendata835 psql -Upg -dtest -f /docker-entrypoint-initdb.d/KOATUU.opendata835.sql

docker-opendata835-cli:
	docker exec -it koatuu_opendata835 psql -Upg test

docker-opendata835-stop:
	docker stop koatuu_opendata835