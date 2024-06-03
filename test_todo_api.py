import requests
import uuid
from rest_framework import status

# run in with this commands
# - python -m pytest -v -s ./file_name::test_name
# - python -m pytest -v -s

ENDPOINT = "https://todo.pixegami.io"

response = requests.get(ENDPOINT)
print(response)

data = response.json()
print(data)

status_code = response.status_code
print(status_code)


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
    # assert response.status_code == status.HTTP_200_OK


def test_can_create_task():
    payload = new_task_payload()
    # json payload is the request body tha this API needs as a JSON object
    put_task_response = requests.put(ENDPOINT + '/create-task', json=payload)
    assert response.status_code == 200

    data = response.json()
    # print(data) # use this if you do not have sure

    task_id = data["task"]["task_id"]
    get_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}")

    assert get_task_response.status_code == 200
    # comparing the task found with the task created 'payload'
    get_task_response = get_task_response.json()
    assert get_task_response["content"] == payload["content"]
    assert get_task_response["user_id"] == payload["user_id"]


def test_can_update_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "content to test",
        "is_done": True
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]


def test_can_delete_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task_id"]

    delete_task_response = delete_task(task_id)
    assert  delete_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404


def test_task_can_list_tasks():
    num = 3
    payload = new_task_payload()
    for _ in range(num):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

        user_id = payload["user_id"]
        list_tasks_response = list_tasks(user_id)
        assert list_tasks_response.status_code == 200
        data = list_tasks_response.json()

        tasks = data["tasks"]
        assert len(tasks == num)


# create functions to not repeat codes

def create_task(payload):
    return requests.post(ENDPOINT + '/create-task', json=payload)


def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")


def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")


def update_task(payload):
    return requests.put(ENDPOINT + '/update-task', json=payload)


def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    return {
        "user_id": user_id,
        # "task_id": "string",
        "content": content,
        "is_done": True
    }


def list_tasks(task_id):
    return requests.get(ENDPOINT + f"/list-tasks/{task_id}")
