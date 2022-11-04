import {initializeAddSet} from "./add-set.js";
import {updateSetDisplay} from "./set-display.js";
import {ApiClient} from "./api-client.js";

window.onload = main();

function main() {
    const apiClient = new ApiClient('http://localhost:8000/api')
    initializeAddSet(apiClient, updateSetDisplay);
}
