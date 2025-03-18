import requests

# URL сервера
url = "http://localhost:5000/tasks"

# Получение всех задач
def get_all_tasks():
    response = requests.get(url)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Ошибка: {response.status_code}")

# Добавление новой задачи
def create_new_task(title):
    new_task = {"title": title}
    response = requests.post(url, json=new_task)
    if response.status_code == 201:
        print(response.json())
    else:
        print(f"Ошибка: {response.status_code}")

# Обновление задачи
def update_task(task_id, title=None, done=None):
    task_url = f"{url}/{task_id}"
    updated_task = {}
    if title:
        updated_task["title"] = title
    if done is not None:
        updated_task["done"] = done
    response = requests.put(task_url, json=updated_task)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Ошибка: {response.status_code}")

# Удаление задачи
def delete_task(task_id):
    task_url = f"{url}/{task_id}"
    response = requests.delete(task_url)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Ошибка: {response.status_code}")

# Пример использования
if __name__ == '__main__':
    get_all_tasks()
    create_new_task("Новая задача")
    update_task(1, done=True)
    delete_task(2)
