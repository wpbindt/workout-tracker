from __future__ import annotations
from typing import Type

from workout_tracker.api.add_exercise import AddExercise
from workout_tracker.api.add_set import AddSet
from workout_tracker.service.executors.add_exercise import AddExerciseExecutor
from workout_tracker.service.executors.add_set import AddSetExecutor
from workout_tracker.api.get_exercise import GetExercise
from workout_tracker.service.executors.get_exercise import GetExerciseExecutor
from workout_tracker.api.get_set import GetSet
from workout_tracker.service.executors.get_set import GetSetExecutor
from workout_tracker.api.get_workout import GetWorkout
from workout_tracker.service.executors.get_workout import GetWorkoutExecutor
from workout_tracker.api.list_exercises import ListExercises
from workout_tracker.service.executors.list_exercises import ListExercisesExecutor
from workout_tracker.api.request import ResponseType, Request, RequestExecutor
from workout_tracker.api.start_workout import StartWorkout
from workout_tracker.service.executors.start_workout import StartWorkoutExecutor
from workout_tracker.repositories.repository import Repositories


class UnknownRequest(Exception):
    pass


class App:
    def __init__(
        self,
        repositories: Repositories
    ) -> None:
        self._repositories = repositories
        self._executors: dict[Type[Request], RequestExecutor[Request, ResponseType]] = {
            GetSet: GetSetExecutor(),
            GetExercise: GetExerciseExecutor(),
            AddSet: AddSetExecutor(),
            StartWorkout: StartWorkoutExecutor(),
            GetWorkout: GetWorkoutExecutor(),
            ListExercises: ListExercisesExecutor(),
            AddExercise: AddExerciseExecutor(),
        }

    async def execute(self, request: Request[ResponseType]) -> ResponseType:
        try:
            executor = self._executors[type(request)]
        except KeyError as e:
            raise UnknownRequest from e
        return await executor.execute(request, self._repositories)
