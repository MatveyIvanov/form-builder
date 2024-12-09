PROJECT_NAME=formbuilder

localup:
	docker compose -f docker/docker-compose.local.yml up --remove-orphans
localbuild:
	docker compose -f docker/docker-compose.local.yml build --no-cache
developup:
	docker compose -f docker/docker-compose.yml up --remove-orphans
developbuild:
	docker compose -f docker/docker-compose.yml build --no-cache
test:
	docker exec -it $(PROJECT_NAME)-asgi pytest .
lint:
	docker exec -it $(PROJECT_NAME)-asgi flake8 .
typecheck:
	docker exec -it $(PROJECT_NAME)-asgi mypy .
black:
	docker exec -it $(PROJECT_NAME)-asgi black .
isort:
	docker exec -it $(PROJECT_NAME)-asgi isort . --profile black --filter-files
