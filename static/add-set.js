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
    const exercises = JSON.parse(setForm.dataset.exercises);
    const selectedExercise = exercises[setData['selected-exercise']];

    return formatSet(
        setData,
        selectedExercise['difficulty_unit'],
        selectedExercise['rep_unit'],
    );
}

function getWorkoutIdFromURL() {
    const params = (new URL(document.location)).searchParams;
    return params.get("id");
}

function formatSet(setData, difficultyUnit, repUnit) {
    return {
        exercise_id: setData['selected-exercise'],
        difficulty: {amount: parseFloat(setData['difficulty']), unit: difficultyUnit},
        intended_reps: {amount: parseFloat(setData['intended-reps']), unit: repUnit},
        actual_reps: {amount: parseFloat(setData['actual-reps']), unit: repUnit},
    }
}
