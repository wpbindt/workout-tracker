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
    const row = setDisplayTable.insertRow(-1);
    const cellContents = [
        exerciseName,
        set.actual_reps.amount.toString(),
        set.intended_reps.amount.toString(),
    ]
    for (const [cellNumber, cellContent] of cellContents.entries()) {
        const cell = row.insertCell(cellNumber);
        cell.innerHTML = cellContent;
    }
}
