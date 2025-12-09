import pytest
from employee_api import EmployeeApi


api = EmployeeApi()


def test_create_employee():
    payload = {
        "name": "Alex",
        "age": 28,
        "position": "QA Engineer"
    }

    response = api.create_employee(payload)
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert data["name"] == payload["name"]


def test_get_employee_info():
    # сначала создаём сотрудника
    payload = {
        "name": "TestUser",
        "age": 30,
        "position": "Developer"
    }
    created = api.create_employee(payload).json()
    emp_id = created["id"]

    # теперь запрашиваем
    response = api.get_employee_info(emp_id)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == emp_id
    assert data["name"] == payload["name"]


def test_update_employee():
    # создаём сотрудника
    employee = api.create_employee({
        "name": "John",
        "age": 35,
        "position": "Manager"
    }).json()
    emp_id = employee["id"]

    # обновляем сотрудника
    updated_payload = {"position": "Senior Manager"}

    response = api.update_employee(emp_id, updated_payload)
    assert response.status_code == 200

    data = response.json()
    assert data["position"] == updated_payload["position"]

    # Проверяем через GET
    check = api.get_employee_info(emp_id).json()
    assert check["position"] == updated_payload["position"]
