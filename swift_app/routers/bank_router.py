from fastapi import APIRouter, Depends

from ..services.bank_service import BankService, get_bank_service
from ..schemas.bank_schemas import BankCreate


bank_router = APIRouter(prefix="/v1/swift-codes")


@bank_router.get("/{swift_code}")
async def get_bank_details(
    swift_code: str, bank_service: BankService = Depends(get_bank_service)
):
    return await bank_service.get_bank_details(swift_code)


@bank_router.get("/country/{countryISO2_code}")
async def get_bank_by_coutry(
    countryISO2_code: str, bank_service: BankService = Depends(get_bank_service)
):
    return await bank_service.get_banks_by_country(countryISO2_code)


@bank_router.post("/")
async def add_new_bank(
    bank: BankCreate, bank_service: BankService = Depends(get_bank_service)
):
    return await bank_service.add_bank(bank)


@bank_router.delete("/{swift_code}")
async def delete_bank(
    swift_code: str, bank_service: BankService = Depends(get_bank_service)
):
    return await bank_service.delete_bank(swift_code)
