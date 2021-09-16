tag = kms
test_image = $(tag)-tests

generate:
	java -jar ./tools/openapi-generator-cli.jar generate \
	  -i ./specs/openapi.yaml \
	  -g python-flask \
	  -o ./src

build:
ifeq ($(new), true)
	docker rmi $(tag)
endif
	docker build -t $(tag) src

DEBUG ?= 0
run:
	docker run --rm -v $(shell pwd)/data:/data -it -p 8000:8000 -e DEBUG=$(DEBUG) $(tag) $(cmd)

build_tests:
ifeq ($(new), true)
	docker rmi $(test_image)
endif
	docker build -t $(test_image) -f src/tests.Dockerfile src

test:
	docker run --rm -it $(test_image) $(args)

clean:
	docker system prune -f --volumes