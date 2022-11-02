function startWorkout() {
    fetch(
        "http://localhost:8000/api/workout",
        {method: "POST"}
    ).then(
        response => response.json()
    ).then(
        response => {
            window.location = "http://localhost:8000/workout?id=" + response.id;
        }
    )
}

export function initializeStartWorkoutButton() {
    const workoutButton = document.getElementById("start-workout-button");
    workoutButton.addEventListener("click", startWorkout);
}
