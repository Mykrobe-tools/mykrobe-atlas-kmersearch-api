#!/usr/bin/env bash

docker run --rm -v $(pwd)/data:/data -it -p 8000:8000 kms