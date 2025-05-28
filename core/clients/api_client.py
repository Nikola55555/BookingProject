import requests
import os
from dotenv import load_dotenv
from requests import Session
from requests.auth import HTTPBasicAuth

from core.settings.environments import Environment
from core.clients.endpoints import Endpoints
from core.settings.config import Users, Timeouts
import allure

load_dotenv()


class APIClient:
    def __init__(self):
        environment_str = os.getenv("Environment", "test")
        try:
            self.environment = Environment(environment_str.lower())
        except KeyError:
            raise ValueError(f"Unsupported environment value: {environment_str}. Use 'test' or 'production'")
        self.base_url = self.get_base_url(self.environment)
        self.session = requests.Session()
        self.session.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv("TEST_BASE_URL")
        elif environment == Environment.PROD:
            return os.getenv("PROD_BASE_URL")
        else:
            raise ValueError(f"Unsupported environment: {environment}")

    def get(self, endpoint, params=None, status_code=200):
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params, headers=self.session.headers)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=data, headers=self.session.headers)
        if status_code:
            assert response.status_code == status_code
            return response


    def ping(self):
        with allure.step("Ping api client"):
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT.value}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step("Assert status code"):
            assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"
        return response.status_code


    def auth(self):
        with allure.step("Getting authenticate"):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT.value}"
            payload = {"username": Users.USERNAME.value, "password": Users.PASSWORD.value}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT.value)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        token = response.json().get("token")
        with allure.step("Updating header with authorization"):
            self.session.headers.update({"Authorization": f"Bearer {token}"})


    def get_booking_by_id(self, booking_id):
        with allure.step("Getting booking"):
            self.session.headers.update({
                "Accept": "application/json"
            })
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response.json()


    def delete_booking(self, booking_id):
        with allure.step("Deleting booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.delete(url, auth=HTTPBasicAuth(Users.USERNAME.value, Users.PASSWORD.value))
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 201, f"Expected status code 200 but got {response.status_code}"
        return response.status_code == 201


    def create_booking(self, booking_data):
        with allure.step("Creating booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}"
            response = self.session.post(url, json=booking_data)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response


    def get_booking_ids(self, param=None):
        with allure.step("Getting object with bookings"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}"
            response = self.session.get(url, params=param)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response


    def update_booking(self, booking_id, booking_data):
        with allure.step("Updating booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.put(url, json=booking_data)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response


    def partial_update_booking(self, booking_id, booking_data):
        with allure.step(" Partial updating booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.patch(url, json=booking_data)
        response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
