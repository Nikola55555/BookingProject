import allure
import pytest
from dotenv import load_dotenv

load_dotenv()


@allure.feature("Test Create Booking")
@allure.story("Test success create booking")
def test_create_booking_with_valid_data_should_return_200(api_client, generate_random_booking_data):
    response = api_client.create_booking(generate_random_booking_data)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    data = response.json()
    assert "bookingid" in data, f"Expected 'bookingid' key in data"
    assert data["booking"]["firstname"] == generate_random_booking_data[
        "firstname"], f"Expected {generate_random_booking_data["firstname"]} in data"


@allure.feature("Test Create Booking")
@allure.story("Test missing required fields")
def test_missing_required_fields(api_client, generate_booking_data_without_required_field):
    response = api_client.create_booking(generate_booking_data_without_required_field)
    try:
        response = api_client.create_booking(generate_booking_data_without_required_field)
        assert response.status_code == 500
    except response.exceptions.HTTPError as e:
        assert e.response.status_code == 500
