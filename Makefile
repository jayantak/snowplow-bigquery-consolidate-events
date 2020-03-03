VERSION?=$(shell git describe --tags --abbrev=0)
IMAGE=snowplow-bigquery-consolidate-events

all: build

build:
	docker build -t $(IMAGE):${VERSION} -f ops/Dockerfile .
	docker tag $(IMAGE):${VERSION} $(IMAGE):latest