from __future__ import annotations
from typing import Type

from workout_tracker.internal_api.add_set import AddSetExecutor, AddSet
from workout_tracker.internal_api.get_exercise import GetExercise, GetExerciseExecutor
from workout_tracker.internal_api.get_set import GetSet, GetSetExecutor
from workout_tracker.internal_api.get_workout import GetWorkoutExecutor, GetWorkout
from workout_tracker.internal_api.list_exercises import ListExercisesExecutor, ListExercises
from workout_tracker.internal_api.request import ResponseType, Request, RequestExecutor
from workout_tracker.internal_api.start_workout import StartWorkoutExecutor, StartWorkout
from workout_tracker.repositories.repository import Repositories


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
        }

    async def execute(self, request: Request[ResponseType]) -> ResponseType:
        return await self._executors[type(request)].execute(request, self._repositories)
