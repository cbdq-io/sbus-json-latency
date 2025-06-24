.EXPORT_ALL_VARIABLES:

TAG = 0.1.0

all: lint build test

build:
	docker compose build --quiet

changelog:
	docker run --quiet --rm --volume "${PWD}:/mnt/source" --workdir /mnt/source ghcr.io/cbdq-io/gitchangelog > CHANGELOG.md

clean:
	docker compose down -t 0 --remove-orphans

lint:
	yamllint -s .
	isort .
	flake8
	bandit -qr .
	docker run --rm -i hadolint/hadolint < Dockerfile

tag:
	@echo $(TAG)

test:
	docker compose run --rm isready
	./peek_topic_messages.py -c 'Endpoint=sb://localhost;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=SAS_KEY_VALUE;UseDevelopmentEmulator=true;' -s test -t test -d
	docker compose up -d sbus-json-latency
	pytest -v
