import {initializeStartWorkoutButton} from "./start-workout-button.js";
import {ApiClient} from "./api-client.js";

window.onload = main();

function main() {
    const apiClient = new ApiClient('http://localhost:8000/api')
    initializeStartWorkoutButton(apiClient);
}
