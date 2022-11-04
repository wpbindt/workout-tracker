async function workoutCallback(apiClient) {
    const workoutId = await apiClient.startWorkout();
    window.location = "http://localhost:8000/workout?id=" + workoutId;
}

export function initializeStartWorkoutButton(apiClient) {
    const workoutButton = document.getElementById("start-workout-button");
    workoutButton.addEventListener(
        "click",
        async () => await workoutCallback(apiClient),
    );
}
