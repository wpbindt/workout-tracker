import {initializeAddSet} from "./add-set.js";
import {updateSetDisplay} from "./set-display.js";

window.onload = main();

function main() {
    initializeAddSet(updateSetDisplay);
}
