import pytest
from pydantic import ValidationError

from ..schemas.bank_schemas import BankCreate


@pytest.fixture
def valid_bank_data():
    return {
        "swiftCode": "NEWBANKKXXX",
        "bankName": "New Bank",
        "address": "123 Street",
        "countryISO2": "US",
        "countryName": "UNITED STATES",
        "isHeadquarter": True,
    }


def prepare_invalid_data(base_data, **overrides):
    return {**base_data, **overrides}


@pytest.mark.parametrize(
    "invalid_swift_code",
    [
        "smalletters",
        "TOSHORT",
        "EXTREMLYWAYTOOLONG",
    ],
)
def test_swift_code_validation(valid_bank_data, invalid_swift_code):
    # Given
    invalid_data = prepare_invalid_data(valid_bank_data, swiftCode=invalid_swift_code)

    # When/Then
    with pytest.raises(ValidationError) as exc_info:
        BankCreate(**invalid_data)

    # Optional
    errors = exc_info.value.errors()
    assert len(errors) == 1


@pytest.mark.parametrize(
    "invalid_country_code",
    ["TOLONG", "S", "54", ""],
)
def test_country_code_validation(valid_bank_data, invalid_country_code):
    # Given
    invalid_data = prepare_invalid_data(
        valid_bank_data, countryISO2=invalid_country_code
    )

    # When/Then
    with pytest.raises(ValidationError) as exc_info:
        BankCreate(**invalid_data)

    # Optional
    errors = exc_info.value.errors()
    assert len(errors) == 1


@pytest.mark.parametrize(
    "invalid_country_name",
    [
        "smalletters",
        "2424234234234",
    ],
)
def test_country_name_validation(valid_bank_data, invalid_country_name):
    # Given
    invalid_data = prepare_invalid_data(
        valid_bank_data, countryName=invalid_country_name
    )

    # When/Then
    with pytest.raises(ValidationError) as exc_info:
        BankCreate(**invalid_data)

    # Optional
    errors = exc_info.value.errors()
    assert len(errors) == 1


@pytest.mark.parametrize(
    "invalid_headquarter_code",
    [
        "ASDBCSDMXK",
        "ASDBCSDMXX",
    ],
)
def test_is_headquarter_validation(valid_bank_data, invalid_headquarter_code):
    # Given
    invalid_data = prepare_invalid_data(
        valid_bank_data, swiftCode=invalid_headquarter_code
    )

    # When/Then
    with pytest.raises(ValidationError) as exc_info:
        BankCreate(**invalid_data)

    # Optional
    errors = exc_info.value.errors()
    assert len(errors) == 1


def test_is_branch_validation(valid_bank_data):
    # Given
    invalid_data = prepare_invalid_data(
        valid_bank_data, swiftCode="ASDBCSDMXXX", isHeadquarter=False
    )

    # When/Then
    with pytest.raises(ValidationError) as exc_info:
        BankCreate(**invalid_data)

    # Optional
    errors = exc_info.value.errors()
    assert len(errors) == 1
