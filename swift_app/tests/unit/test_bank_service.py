import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException, status

from ...services.bank_service import BankService
from ...repositories.bank_repository import BankRepository
from ...schemas.bank_schemas import BankCreate


@pytest.fixture
def mock_headquarter_bank_data():
    return {
        "swiftCode": "FDABCDUSXXX",
        "bankName": "Test Bank HQ",
        "address": "123 Main St",
        "countryISO2": "US",
        "countryName": "UNITED STATES",
        "isHeadquarter": True,
    }


@pytest.fixture
def mock_branch_bank_data():
    return {
        "swiftCode": "FDABCDUSNYV",
        "bankName": "Test Bank NY Branch",
        "address": "456 Broadway",
        "countryISO2": "US",
        "countryName": "UNITED STATES",
        "isHeadquarter": False,
    }


@pytest.fixture
def mock_bank_repository():
    return AsyncMock(spec=BankRepository)


@pytest.fixture
def bank_service(mock_bank_repository):
    return BankService(bank_repository=mock_bank_repository)


@pytest.fixture
def mock_headquarter_bank(mock_headquarter_bank_data):
    mock = MagicMock()
    for key, value in mock_headquarter_bank_data.items():
        setattr(mock, key, value)
    return mock


@pytest.fixture
def mock_branch_bank(mock_branch_bank_data):
    mock = MagicMock()
    for key, value in mock_branch_bank_data.items():
        setattr(mock, key, value)
    return mock


@pytest.mark.asyncio
async def test_get_bank_details_headquarter(
    bank_service, mock_bank_repository, mock_headquarter_bank
):
    mock_bank_repository.get_bank_by_swift.return_value = mock_headquarter_bank

    result = await bank_service.get_bank_details("FDABCDUSXXX")

    assert result.status_code == status.HTTP_200_OK
    mock_bank_repository.get_bank_by_swift.assert_called_once_with("FDABCDUSXXX")
    mock_bank_repository.get_bank_branches.assert_called_once_with("FDABCDUS")


@pytest.mark.asyncio
async def test_get_bank_details_branch(
    bank_service, mock_bank_repository, mock_branch_bank
):
    mock_bank_repository.get_bank_by_swift.return_value = mock_branch_bank

    result = await bank_service.get_bank_details("FDABCDUSNYV")

    assert result.status_code == status.HTTP_200_OK
    mock_bank_repository.get_bank_by_swift.assert_called_once_with("FDABCDUSNYV")
    mock_bank_repository.get_bank_branches.assert_not_called()


@pytest.mark.asyncio
async def test_get_bank_details_not_found(bank_service, mock_bank_repository):
    mock_bank_repository.get_bank_by_swift.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await bank_service.get_bank_details("INVALIDCXXX")

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_banks_by_country_success(
    bank_service, mock_bank_repository, mock_headquarter_bank, mock_branch_bank
):
    mock_bank_repository.get_banks_by_country_code.return_value = [
        mock_headquarter_bank,
        mock_branch_bank,
    ]

    result = await bank_service.get_banks_by_country("US")

    assert result.status_code == status.HTTP_200_OK
    mock_bank_repository.get_banks_by_country_code.assert_called_once_with("US")


@pytest.mark.asyncio
async def test_get_banks_by_country_not_found(bank_service, mock_bank_repository):
    mock_bank_repository.get_banks_by_country_code.return_value = []

    with pytest.raises(HTTPException) as exc_info:
        await bank_service.get_banks_by_country("XX")

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_add_bank_success(bank_service, mock_bank_repository):
    bank_data = BankCreate(
        swiftCode="NEWBANKKXXX",
        bankName="New Bank",
        address="123 Street",
        countryISO2="US",
        countryName="UNITED STATES",
        isHeadquarter=True,
    )

    mock_bank_repository.get_bank_by_swift.return_value = None
    mock_bank_repository.add_bank.return_value = None

    result = await bank_service.add_bank(bank_data)

    assert result.status_code == status.HTTP_201_CREATED
    mock_bank_repository.get_bank_by_swift.assert_called_once_with("NEWBANKKXXX")
    mock_bank_repository.add_bank.assert_called_once()


@pytest.mark.asyncio
async def test_add_bank_conflict(
    bank_service, mock_bank_repository, mock_headquarter_bank
):
    bank_data = BankCreate(
        swiftCode="FDABCDUSXXX",
        bankName="Existing Bank",
        address="123 Street",
        countryISO2="US",
        countryName="UNITED STATES",
        isHeadquarter=True,
    )

    mock_bank_repository.get_bank_by_swift.return_value = mock_headquarter_bank

    with pytest.raises(HTTPException) as exc_info:
        await bank_service.add_bank(bank_data)

    assert exc_info.value.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_delete_bank_success(
    bank_service, mock_bank_repository, mock_headquarter_bank
):
    mock_bank_repository.get_bank_by_swift.return_value = mock_headquarter_bank
    mock_bank_repository.delete_bank.return_value = None

    result = await bank_service.delete_bank("FDABCDUSXXX")

    assert result.status_code == status.HTTP_200_OK
    mock_bank_repository.get_bank_by_swift.assert_called_once_with("FDABCDUSXXX")
    mock_bank_repository.delete_bank.assert_called_once_with("FDABCDUSXXX")


@pytest.mark.asyncio
async def test_delete_bank_not_found(bank_service, mock_bank_repository):
    mock_bank_repository.get_bank_by_swift.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await bank_service.delete_bank("NONEXISTXXX")

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
