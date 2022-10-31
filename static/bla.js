fetch(
    'http://localhost:8000/workout',
).then((response) => response.json())
    .then(
    (response) => {
        const stuffElement = document.getElementById("putstuffhere");
        for (const workout of response) {
            const bla = document.createTextNode(workout.time);
            const a = document.createElement('a');
            a.title = "my title text";
            a.href = "workout.html?id=" + workout.id;
            const p = document.createElement('p');
            a.appendChild(bla);
            p.appendChild(a);
            stuffElement.appendChild(p);
        }
    }
)

const addButton = document.getElementById('start');
addButton.addEventListener("click", (event) => {
    fetch(
        'http://localhost:8000/workout',
        {method: 'POST'}
    ).then((response) => response.json())
    .then((response) => {
        window.location = "workout.html?id=" + response.id;
    }).then()
});