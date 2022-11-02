export function initializeAddSet(setAddedCallback) {
    const addSetButton = document.getElementById('add-set');
    addSetButton.addEventListener('click', addSet(setAddedCallback));
}

function addSet(setAddedCallback) {
    return () => {
        const set = getSetFromForm();
        const workoutId = getWorkoutIdFromURL();
        postSetToAPI(set, workoutId).then(setAddedCallback);
    }
}

function getSetFromForm() {
    const setForm = document.getElementById('set-input-form');
    const setData = Object.fromEntries(new FormData(setForm).entries());
    return formatSet(setData);
}

function getWorkoutIdFromURL() {
    const params = (new URL(document.location)).searchParams;
    return params.get("id");
}

function formatSet(setData) {
    return {
        exercise_id: setData['selected-exercise'],
        difficulty: {amount: parseFloat(setData['difficulty']), unit: 'kg'},
        intended_reps: {amount: parseFloat(setData['intended-reps']), unit: 'repetition'},
        actual_reps: {amount: parseFloat(setData['actual-reps']), unit: 'repetition'},
    }
}

function postSetToAPI(set, workoutId) {
    return fetch(
        "http://localhost:8000/workout/" + workoutId,
        {
            method: "PATCH",
            body: JSON.stringify(set),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            }
        }
    ).then(
        response => response.json()
    ).then(
        set => set.id
    )
}
