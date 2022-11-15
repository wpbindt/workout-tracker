.PHONY: build-image
build-image:
	docker build --rm -f workout-tracker.dockerfile -t workout-tracker .

.PHONY: run-mypy
run-mypy: build-image
	docker run -v $(shell pwd):/srv workout-tracker mypy .

.PHONY: run-integration-tests
run-integration-tests: build-image
	docker-compose -f docker-compose.test.yml up -d;
	docker run --network workout_app_test_network -v $(shell pwd):/srv workout-tracker pytest tests/integration

.PHONY: run-unit-tests
run-unit-tests: build-image
	docker run -v $(shell pwd):/srv workout-tracker pytest tests/unit

.PHONY: run-tests
run-tests: run-integration-tests run-unit-tests
