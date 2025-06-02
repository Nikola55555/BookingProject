import allure
import pytest
from dotenv import load_dotenv
from pydantic import ValidationError
from core.models.booking import BookingResponse

load_dotenv()


@allure.feature("Test Create Booking")
@allure.story("Positive: create booking with custom data")
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "James",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }

    response = api_client.create_booking(booking_data).json()
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature("Test Create Booking")
@allure.story("Test success create booking")
def test_create_booking_with_random_valid_data(api_client, generate_random_booking_data):
    response = api_client.create_booking(generate_random_booking_data).json()
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response['booking']['firstname'] == generate_random_booking_data['firstname']
    assert response['booking']['lastname'] == generate_random_booking_data['lastname']
    assert response['booking']['totalprice'] == generate_random_booking_data['totalprice']
    assert response['booking']['depositpaid'] == generate_random_booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == generate_random_booking_data['bookingdates']['checkin']
    generate_random_booking_data

@allure.feature("Test Create Booking")
@allure.story("Test create booking with invalid firstname type")
def test_create_booking_with_invalid_firstname_type(api_client, generate_random_booking_data):
    test_data = generate_random_booking_data
    test_data["firstname"] = 5

    with pytest.raises(Exception, match="Internal Server Error"):
        api_client.create_booking(generate_random_booking_data).json()


@allure.feature("Test Create Booking")
@allure.story("Test create booking with invalid lastname type")
def test_create_booking_with_invalid_lastname_type(api_client, generate_random_booking_data):
    test_data = generate_random_booking_data
    test_data["lastname"] = 5

    with pytest.raises(Exception, match="Internal Server Error"):
        api_client.create_booking(test_data).json()


@allure.feature("Test Create Booking")
@allure.story("Test create booking with invalid bookingdates type")
def test_create_booking_with_invalid_bookingdates_type(api_client, generate_random_booking_data):
    test_data = generate_random_booking_data
    test_data['bookingdates'] = 55556
    with pytest.raises(Exception, match="Internal Server Error"):
        api_client.create_booking(test_data).json()


@allure.feature("Test Create Booking")
@allure.story("Test create booking with empty lastname")
def test_create_booking_with_empty_lastname(api_client, generate_random_booking_data):
    test_data = generate_random_booking_data
    test_data["lastname"] = ''
    response = api_client.create_booking(test_data).json()
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")


@allure.feature("Test Create Booking")
@allure.story("Test create booking with empty firstname")
def test_create_booking_with_empty_firstname(api_client, generate_random_booking_data):
    test_data = generate_random_booking_data
    test_data["firstname"] = ''
    response = api_client.create_booking(test_data).json()
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")



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
