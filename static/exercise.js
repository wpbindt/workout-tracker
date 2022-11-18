const addExerciseButton = document.getElementById('add-exercise');

addExerciseButton.addEventListener('click', showExerciseForm);

function showExerciseForm (event) {
    event.preventDefault();
    addExerciseButton.disabled = true;
    const exerciseTable = document.getElementById('exercise-table');
    const row = exerciseTable.insertRow(1);

    const cellIds = [
        'name-field',
        'difficulty-field',
        'rep-field',
        'description-field',
    ]

    for (const [cellNumber, cellId] of cellIds.entries()) {
        const cell = row.insertCell(cellNumber);
        const inputElt = document.createElement('input');
        inputElt.type = 'text';
        inputElt.id = cellId;
        cell.appendChild(inputElt);
    }
    const cell = row.insertCell(4);
    const addButton = document.createElement('button');
    addButton.innerText = 'Add';
    cell.appendChild(addButton);
}
