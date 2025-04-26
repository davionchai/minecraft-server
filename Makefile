.PHONY: up
up:
	docker compose up -d

.PHONY: down
down:
	docker compose down --remove-orphans -v

.PHONY: logs
logs:
	docker compose logs -f -t

.PHONY: exec
exec:
	docker exec -it minecraft bash
