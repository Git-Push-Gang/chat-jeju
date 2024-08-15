all: prep update_requirements
	@docker compose -f ./srcs/docker-compose.yml up -d --build

down:
	@docker compose -f ./srcs/docker-compose.yml down

re: prep update_requirements
	@docker compose -f srcs/docker-compose.yml up -d --build

clean:
	@if [ -n "$$(docker ps -qa)" ]; then \
		docker stop $$(docker ps -qa); \
		docker rm $$(docker ps -qa); \
	fi
	@if [ -n "$$(docker images -qa)" ]; then \
		docker rmi -f $$(docker images -qa); \
	fi
	@if [ -n "$$(docker volume ls -q)" ]; then \
		docker volume rm $$(docker volume ls -q); \
	fi
	@docker network ls | tail -n +2 | awk '$$2 !~ /bridge|none|host/' | awk '{ print $$1 }' | xargs -r -I {} docker network rm {}

update_requirements:
	@pip freeze > srcs/solar-backend-fastapi/config/requirements.txt

prep:
	@if [ ! -d "/home/$$USER/chroma-data" ]; then \
		mkdir -p /home/$$USER/chroma-data; \
	fi
	@if [ ! -d "/home/$$USER/proxy/srcs/chroma" ]; then \
		git -C /home/$$USER/proxy/srcs clone https://github.com/chroma-core/chroma.git chroma; \
	fi

local: down update_requirements
	@docker compose -f ./srcs/docker-compose.yml up -d --build

.PHONY: all re down clean prep local update_requirements