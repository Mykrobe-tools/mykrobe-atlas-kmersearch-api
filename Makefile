tag = kms

generate:
	java -jar ./tools/openapi-generator-cli.jar generate \
	  -i ./specs/openapi.yaml \
	  -g python-flask \
	  -o ./src

build:
	docker build -t $(tag) src

run:
	docker run --rm -v $(shell pwd)/data:/data -it -p 8080:8080 $(tag)