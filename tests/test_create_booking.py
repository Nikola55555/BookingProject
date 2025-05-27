import allure
import pytest
import requests
from core.clients.endpoints import Endpoints
import os
from dotenv import load_dotenv
from core.clients import endpoints


load_dotenv()


@allure.feature("Test Create Booking")
@allure.story("Test success create booking")
def test_create_booking_with_valid_data_should_return_200(api_client, generate_random_booking_data):
    print(f"Base URL: {api_client.base_url}")
    response = api_client.create_booking(generate_random_booking_data)
    #response = api_client.post("booking", data=generate_random_booking_data, status_code=200)
    print(response)
