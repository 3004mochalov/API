from flask import Flask, jsonify, request

app = Flask(__name__)

# Простой список задач
tasks = [
    {"id": 1, "title": "Задача 1", "done": False},
    {"id": 2, "title": "Задача 2", "done": False}
]

# GET запрос для получения всех задач
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# POST запрос для добавления новой задачи
@app.route('/tasks', methods=['POST'])
def create_task():
    new_task = {
        "id": len(tasks) + 1,
        "title": request.json["title"],
        "done": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

# PUT запрос для обновления задачи
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Задача не найдена"}), 404
    task["title"] = request.json.get("title", task["title"])
    task["done"] = request.json.get("done", task["done"])
    return jsonify(task)

# DELETE запрос для удаления задачи
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Задача не найдена"}), 404
    tasks.remove(task)
    return jsonify({"message": "Задача удалена"})

if __name__ == '__main__':
    app.run(debug=True)
