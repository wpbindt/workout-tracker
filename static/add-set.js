export function initializeAddSet(apiClient, setAddedCallback) {
    const addSetButton = document.getElementById('add-set');
    addSetButton.addEventListener('click', addSet(apiClient, setAddedCallback));
}

function addSet(apiClient, setAddedCallback) {
    return async () => {
        const set = getSetFromForm();
        const workoutId = getWorkoutIdFromURL();
        const setId = await apiClient.addSet(set, workoutId);
        setAddedCallback(setId);
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
