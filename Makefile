.PHONY: up build extract-locales sync

up:
	docker compose up

build:
	docker compose up --build

extract-locales:
	uv run fast-ftl-extract \
	'./app' \
	'./app/i18n/locales' \
	-l 'uk' \
	-l 'en' \
	-l 'ru' \
	-K 'LF' \
	-I 'core' \
	-I 'manager' \
	-p self \
	--comment-junks \
	--comment-keys-mode 'comment' \
	--verbose

sync:
	uv sync --extra dev --extra lint

migrate-create:
	uv run alembic revision --autogenerate -m "$(m)"

migrate-up:
	uv run alembic upgrade head

migrate-down:
	uv run alembic downgrade -1
