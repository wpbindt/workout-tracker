export class ApiClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    async makeRequest(path, method, body) {
        const response = await fetch(
            this.baseURL + path,
            {
                method: method,
                body: JSON.stringify(body),
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                },
            }
        );
        return response.json();
    }

    async startWorkout() {
        const workout = await this.makeRequest(
            '/workout',
            'POST',
        );
        return workout.id;
    }

    async addSet(set, workoutId) {
        const returnedSet = await this.makeRequest(
            '/workout/' + workoutId,
            'PATCH',
            set,
        );
        return returnedSet.id;
    }

    async getSet(workoutId, setId) {
        const set = await this.makeRequest(
            "/workout/" + workoutId + '/' + setId
        );
        const exercise = await this.makeRequest(
            "/exercise/" + set.exercise_id
        );
        return {
            set: set,
            exercise: exercise,
        };
    }
}
