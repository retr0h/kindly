#!/usr/bin/env make

PROJECT?=kindly
NAMESPACE?=test
VERSION?=$(shell git describe --tags --always)

CONTAINER?=$(NAMESPACE)/$(PROJECT):$(VERSION)
CONTAINER_LATEST?=$(NAMESPACE)/$(PROJECT):latest

.PHONY: docker-build
docker-build:
	docker build -t $(CONTAINER) .
	docker tag $(CONTAINER) $(CONTAINER_LATEST)
