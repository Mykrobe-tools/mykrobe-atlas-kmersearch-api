tag = kms
test_image = $(tag)-tests

generate:
	java -jar ./tools/openapi-generator-cli.jar generate \
	  -i ./specs/openapi.yaml \
	  -g python-flask \
	  -o ./src

build:
	docker build -t $(tag) src

run:
	docker run --rm -v $(shell pwd)/data:/data -it -p 8000:8000 $(tag)

build_tests:
	docker build -t $(test_image) -f src/tests.Dockerfile src

test:
	docker run --rm -it $(test_image) $(args)

clean:
	docker system prune -f --volumes