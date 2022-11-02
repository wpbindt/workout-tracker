from uuid import UUID

from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from workout_tracker.api import api_router
from workout_tracker.models.exercise import Exercise
from workout_tracker.models.workout import Workout
from workout_tracker.repositories.factory import exercise_repository_factory, workout_repository_factory
from workout_tracker.repositories.repository import Repository

app = FastAPI()

app.include_router(api_router, prefix='/api')

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        'index.html',
        {'request': request},
    )


@app.get('/workout', response_class=HTMLResponse)
async def individual_workout(
    request: Request,
    id: UUID,
    workout_repository: Repository[Workout, UUID] = Depends(workout_repository_factory),
    exercise_repository: Repository[Exercise, UUID] = Depends(exercise_repository_factory),
):
    workout = (await workout_repository.get_by_ids({id}))[id]
    exercises = {exercise.id: exercise async for exercise in exercise_repository.get_all()}
    return templates.TemplateResponse(
        'workout.html',
        {
            'request': request,
            'available_exercises': exercises,
            'workout': workout
        }
    )
