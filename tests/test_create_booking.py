import allure
import pytest
from dotenv import load_dotenv

load_dotenv()


@allure.feature("Test Create Booking")
@allure.story("Test success create booking")
def test_create_booking_with_valid_data(api_client, generate_random_booking_data):
    response = api_client.create_booking(generate_random_booking_data)
    data = response.json()
    assert "bookingid" in data, f"Expected 'bookingid' key in data"
    assert data["booking"]["firstname"] == generate_random_booking_data[
        "firstname"], f"Expected {generate_random_booking_data["firstname"]} in data"


@pytest.mark.parametrize("field_to_remove", ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"])
@allure.feature("Test Create Booking")
@allure.story("Test missing required fields")
def test_missing_required_fields(api_client, generate_random_booking_data, field_to_remove):
    test_data = generate_random_booking_data
    test_data.pop(field_to_remove)
    with pytest.raises(Exception, match="Internal Server Error"):
        api_client.create_booking(test_data)


@allure.feature("Test Create Booking")
@allure.story("Test empty body request")
def test_empty_body_request(api_client):
    with pytest.raises(Exception, match="Internal Server Error"):
        api_client.create_booking({})


@allure.feature("Test Create Booking")
@allure.story("Test numeric input in firstname field")
def test_numeric_input_in_firstname_field(api_client, generate_random_booking_data):
    test_data = generate_random_booking_data
    test_data["firstname"] = 2
    with pytest.raises(Exception, match="Internal Server Error"):
        api_client.create_booking(test_data)
