.PHONY: run stop logs build clean

run:
	docker-compose up -d

stop:
	docker-compose down

logs:
	docker-compose logs -f recipe-bot

build:
	docker-compose up --build -d

clean:
	docker-compose down --volumes --remove-orphans
