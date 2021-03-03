tag = kms

generate:
	java -jar ./tools/openapi-generator-cli.jar generate \
	  -i ./specs/openapi.yaml \
	  -g python-flask \
	  -o ./src

build:
	docker build -t $(tag) src

run:
	docker run --rm -v $(shell pwd)/data:/data -it -p 8000:8000 $(tag)

build_test:
	docker build -t $(tag)_test -f src/test.Dockerfile src

test:
	docker run --rm -v $(shell pwd)/data:/data -it $(tag)_test

clean:
	docker system prune -f --volumes