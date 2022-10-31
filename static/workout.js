const params = (new URL(document.location)).searchParams;
const workoutId = params.get("id");

fetch(
    'http://localhost:8000/workout/' + workoutId,
).then((response) => response.json())
    .then(
        (response) => {
            const tn = document.createTextNode(JSON.stringify(response));
            const divvy = document.getElementById('stuffhere');
            divvy.appendChild(tn);
        }
    )
