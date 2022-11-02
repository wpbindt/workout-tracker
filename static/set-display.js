export function updateSetDisplay(setId) {
    getSetFromAPI(setId).then(
        set => getExerciseNameFromAPI(set)
    ).then(
        response => {
            appendSetToDisplay(...response)
        }
    )
}

function getWorkoutIdFromURL() {
    const params = (new URL(document.location)).searchParams;
    return params.get("id");
}

function getSetFromAPI(setId) {
    const workoutId = getWorkoutIdFromURL()
    return fetch(
        "http://localhost:8000/api/workout/" + workoutId + '/' + setId
    ).then(response => response.json())
}

function getExerciseNameFromAPI(set) {
    return fetch(
        "http://localhost:8000/api/exercise/" + set.exercise_id
    ).then(
        response => response.json()
    ).then(
        exercise => {
            return [set, exercise.name];
        }
    )
}

function appendSetToDisplay(set, exerciseName) {
    const setDisplayTable = document.getElementById("set-display");
    const root = document.createElement('tr');
    const name = document.createElement('td');
    name.appendChild(document.createTextNode(exerciseName));
    const intendedReps = document.createElement('td');
    intendedReps.appendChild(document.createTextNode(set.intended_reps.amount));
    const actualReps = document.createElement('td');
    actualReps.appendChild(document.createTextNode(set.actual_reps.amount));
    root.appendChild(name);
    root.appendChild(actualReps);
    root.appendChild(intendedReps);
    setDisplayTable.appendChild(root);
}
