import requests
from fastapi import status

BASE_URL = "http://localhost:8080"
API_VERSION = "v1"
HEADERS = {"Content-Type": "application/json"}

EXISTING_SWIFT_CODE = "CRLYMCM1FVI"
EXISTING_COUNTRY_ISO2 = "MC"
EXISTING_SWIFT_CODE_DATA = {
    "address": "13 AVENUE DU PRINCE HEREDITAIRE  MONACO, MONACO, 98000",
    "bankName": "LCL (LE CREDIT LYONNAIS) MONACO",
    "countryISO2": "MC",
    "isHeadquarter": False,
    "swiftCode": "CRLYMCM1FVI",
}


def test_retrieve_existing_swift_code():
    response = requests.get(
        f"{BASE_URL}/{API_VERSION}/swift-codes/{EXISTING_SWIFT_CODE}", headers=HEADERS
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["swiftCode"] == EXISTING_SWIFT_CODE
    assert data["bankName"] == EXISTING_SWIFT_CODE_DATA["bankName"]
    assert data["address"] == EXISTING_SWIFT_CODE_DATA["address"]
    assert data["countryISO2"] == EXISTING_SWIFT_CODE_DATA["countryISO2"]
    assert data["isHeadquarter"] == EXISTING_SWIFT_CODE_DATA["isHeadquarter"]


def test_retrieve_nonexistent_swift_code():
    nonexistent_code = "NONEXISTENT123"
    response = requests.get(
        f"{BASE_URL}/{API_VERSION}/swift-codes/{nonexistent_code}", headers=HEADERS
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_retrieve_swift_codes_by_country():
    response = requests.get(
        f"{BASE_URL}/{API_VERSION}/swift-codes/country/{EXISTING_COUNTRY_ISO2}",
        headers=HEADERS,
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["countryISO2"] == EXISTING_COUNTRY_ISO2
    assert isinstance(data["swiftCodes"], list)
    assert len(data["swiftCodes"]) >= 0

    swift_codes = [item["swiftCode"] for item in data["swiftCodes"]]
    assert EXISTING_SWIFT_CODE in swift_codes


def test_retrieve_nonexistent_country():
    nonexistent_country = "XX"
    response = requests.get(
        f"{BASE_URL}/{API_VERSION}/swift-codes/country/{nonexistent_country}",
        headers=HEADERS,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_add_and_delete_swift_code():
    test_swift_code = "EXAMPLE1FVI"
    test_data = {
        "address": "Example address",
        "bankName": "Example bank name",
        "countryISO2": EXISTING_COUNTRY_ISO2,
        "countryName": "MONACO",
        "isHeadquarter": False,
        "swiftCode": test_swift_code,
    }

    response = requests.post(
        f"{BASE_URL}/{API_VERSION}/swift-codes", json=test_data, headers=HEADERS
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "message" in data

    response = requests.get(
        f"{BASE_URL}/{API_VERSION}/swift-codes/{test_swift_code}", headers=HEADERS
    )
    assert response.status_code == status.HTTP_200_OK

    response = requests.delete(
        f"{BASE_URL}/{API_VERSION}/swift-codes/{test_swift_code}", headers=HEADERS
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data

    response = requests.get(
        f"{BASE_URL}/{API_VERSION}/swift-codes/{test_swift_code}", headers=HEADERS
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_add_swift_code_validation():
    invalid_data = {
        "address": "Example address",
        "bankName": "Invalid Bank",
        "countryISO2": "U",
        "countryName": "Invalid Country",
        "isHeadquarter": "not-a-boolean",
        "swiftCode": "",
    }

    response = requests.post(
        f"{BASE_URL}/{API_VERSION}/swift-codes", json=invalid_data, headers=HEADERS
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
