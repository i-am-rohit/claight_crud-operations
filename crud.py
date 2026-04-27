from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []
current_id = 1


def find_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


@app.route('/tasks', methods=['POST'])
def create_task():
    global current_id

    data = request.get_json()

    if not data or not data.get("title") or not data.get("description"):
        return jsonify({"error": "Title and description are required"}), 400

    new_task = {
        "id": current_id,
        "title": data["title"],
        "description": data["description"],
        "completed": False
    }

    tasks.append(new_task)
    current_id += 1

    return jsonify(new_task), 201


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify([
        {
            "id": task["id"],
            "title": task["title"],
            "description": task["description"],
            "completed": task["completed"]
        }
        for task in tasks
    ]), 200


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "id": task["id"],
        "title": task["title"],
        "description": task["description"],
        "completed": task["completed"]
    }), 200


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = find_task(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()

    if "title" in data and not data["title"]:
        return jsonify({"error": "Title cannot be empty"}), 400

    if "description" in data and not data["description"]:
        return jsonify({"error": "Description cannot be empty"}), 400

    task["title"] = data.get("title", task["title"])
    task["description"] = data.get("description", task["description"])
    task["completed"] = data.get("completed", task["completed"])

    return jsonify({
        "id": task["id"],
        "title": task["title"],
        "description": task["description"],
        "completed": task["completed"]
    }), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = find_task(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    tasks.remove(task)
    return jsonify({
        "id": task["id"],
        "title": task["title"],
        "description": task["description"],
        "completed": task["completed"]
    }), 200


if __name__ == '__main__':
    app.run(debug=True)