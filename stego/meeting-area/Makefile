all: clean build run

build:
	./docker-build.sh
	
run:
	./docker-run.sh

restart:
	docker restart $(shell docker ps -q) || true

clean:
	docker system prune -f || true
	docker kill $(shell docker ps -q) || true
	docker rm $(shell docker ps -a -q) || true