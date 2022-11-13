build-image:
	docker build --rm -f workout-tracker.dockerfile -t workout-tracker .

run-server:
	docker run -u 1000:1000 \
		-v $(shell pwd):/srv \
		-p 8000:8000 \
		--network workout_app_test_network \
		workout-tracker \
		uvicorn main:app --reload --port 8000 --host 0.0.0.0

run-mypy:
	docker run -v $(shell pwd):/srv workout-tracker mypy .
