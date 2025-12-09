import requests


class EmployeeApi:
    BASE_URL = "http://5.101.50.27:8000"

    def create_employee(self, payload: dict):
        """
        Создаёт нового сотрудника.
        Метод: POST /employee/create
        Body: JSON
        """
        url = f"{self.BASE_URL}/employee/create"
        response = requests.post(url, json=payload)
        return response

    def get_employee_info(self, employee_id: int):
        """
        Получает информацию о сотруднике.
        Метод: GET /employee/info?id=<ID>
        """
        url = f"{self.BASE_URL}/employee/info"
        response = requests.get(url, params={"id": employee_id})
        return response

    def update_employee(self, employee_id: int, payload: dict):
        """
        Обновляет информацию о сотруднике.
        Метод: PATCH /employee/change
        """
        url = f"{self.BASE_URL}/employee/change"
        payload_with_id = {"id": employee_id, **payload}
        response = requests.patch(url, json=payload_with_id)
        return response
