build-image:
	docker build --rm -f workout-tracker.dockerfile -t workout-tracker .

run-mypy:
	docker run -v $(shell pwd):/srv workout-tracker mypy .
