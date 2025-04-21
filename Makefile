all: lint build test

build:
	docker compose pull --quiet
	docker compose build --quiet

clean:
	docker compose down -t 0 --remove-orphans

lint:
	yamllint -s .
	isort .
	flake8
	bandit -qr .
	docker run --rm -i hadolint/hadolint < Dockerfile

test:
	docker compose run --rm isready
	./peek_topic_messages.py -c 'Endpoint=sb://localhost;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=SAS_KEY_VALUE;UseDevelopmentEmulator=true;' -s test -t test -d
	docker compose up -d sbus-json-latency
