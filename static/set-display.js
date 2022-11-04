export function updateSetDisplay(apiClient) {
    return async (setId) => {
        const workoutId = getWorkoutIdFromURL();
        const setData = await apiClient.getSet(workoutId, setId);
        appendSetToDisplay(setData.set, setData.exercise.name);
    };
}

function getWorkoutIdFromURL() {
    const params = (new URL(document.location)).searchParams;
    return params.get("id");
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
