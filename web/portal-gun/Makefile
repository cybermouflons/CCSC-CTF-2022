
all: clean build run

build:
	./docker-build.sh
	
run:
	./docker-run.sh

clean:
	docker system prune -f || true
	docker-compose -f setup/docker-compose.yml rm -fsv