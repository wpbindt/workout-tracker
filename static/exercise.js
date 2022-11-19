import {ApiClient} from "./api-client.js";

const addExerciseButton = document.getElementById('add-exercise');

addExerciseButton.addEventListener('click', showExerciseForm);

function showExerciseForm (event) {
    event.preventDefault();
    addExerciseButton.disabled = true;
    const exerciseTable = document.getElementById('exercise-table');
    const row = exerciseTable.insertRow(1);

    const cells = [
        row.insertCell(),
        row.insertCell(),
        row.insertCell(),
        row.insertCell(),
    ];

    for (const cell of cells) {
        const inputElement = document.createElement('input');
        inputElement.type = 'text';
        cell.appendChild(inputElement);
    }
    const cell = row.insertCell();
    const addButton = document.createElement('button');
    addButton.innerText = 'Add';
    cell.appendChild(addButton);
    addButton.addEventListener('click', addExercise(cells, addButton))
}

function addExercise (cells, addButton) {
    return async () => {
        const exercise = {
            name: cells[0].firstChild.value,
            difficulty_unit: cells[1].firstChild.value,
            rep_unit: cells[2].firstChild.value,
            description: cells[3].firstChild.value,
        }
        const apiClient = new ApiClient('http://localhost:8000/api');
        await apiClient.addExercise(exercise);
        cells[0].innerText = exercise.name;
        cells[1].innerText = exercise.difficulty_unit;
        cells[2].innerText = exercise.rep_unit;
        cells[3].innerText = exercise.description;
        addExerciseButton.disabled = false;
        addButton.remove();
    }
}
