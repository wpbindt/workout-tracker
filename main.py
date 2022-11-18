import json
from uuid import UUID

from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from workout_tracker.adapters.create_app import create_app
from workout_tracker.adapters.rest_api import api_router
from workout_tracker.app import App
from workout_tracker.api.get_workout import GetWorkout
from workout_tracker.api.list_exercises import ListExercises

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
    workout_app: App = Depends(create_app),
):
    workout = await GetWorkout(id).execute(workout_app)
    exercises = await ListExercises().execute(workout_app)
    return templates.TemplateResponse(
        'workout.html',
        {
            'request': request,
            'available_exercises': {
                str(exercise.id): json.loads((exercise.json()))
                for exercise in exercises.values()
            },
            'workout': json.loads(workout.json()),
        }
    )


@app.get('/exercise', response_class=HTMLResponse)
async def exercises(
    request: Request,
    app: App = Depends(create_app),
) -> templates.TemplateResponse:
    exercises_ = [
        exercise.dict()
        for exercise in (await app.execute(ListExercises())).values()
    ]
    return templates.TemplateResponse(
        'exercise.html',
        {
            'request': request,
            'exercises': exercises_
        }
    )
