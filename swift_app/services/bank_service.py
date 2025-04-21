from fastapi.params import Depends
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from ..repositories.bank_repository import BankRepository, get_bank_repository
from ..schemas.bank_schemas import (
    BasicBankResponse,
    DetailedBankResponse,
    CountryBankResponse,
    BankCreate,
)
from ..models.bank_model import Bank


class BankService:
    def __init__(
        self,
        bank_repository: BankRepository = Depends(get_bank_repository),
    ):
        self.bank_repository = bank_repository

    from fastapi.responses import JSONResponse

    async def get_bank_details(self, swift_code: str):
        existing_bank = await self.bank_repository.get_bank_by_swift(swift_code)
        if not existing_bank:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bank with this SWIFT code doesn't exist",
            )

        if existing_bank.isHeadquarter:
            response_data = DetailedBankResponse.from_orm(existing_bank)
            branches = await self.bank_repository.get_bank_branches(swift_code[:-3])
            response_data.branches = [BasicBankResponse.from_orm(b) for b in branches]
        else:
            response_data = BasicBankResponse.from_orm(existing_bank)

        return JSONResponse(
            status_code=status.HTTP_200_OK, content=response_data.model_dump()
        )

    async def get_banks_by_country(self, countryISO2: str):
        banks = await self.bank_repository.get_banks_by_country_code(countryISO2)

        if not banks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Banks with this country code don't exist",
            )

        response_data = CountryBankResponse(
            countryISO2=countryISO2,
            countryName=banks[0].countryName,
            swiftCodes=[BasicBankResponse.from_orm(bank) for bank in banks],
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK, content=response_data.model_dump()
        )

    async def add_bank(self, bank_data: BankCreate):
        existing_bank = await self.bank_repository.get_bank_by_swift(
            bank_data.swiftCode
        )
        if existing_bank:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Bank with SWIFT code {bank_data.swiftCode} already exists",
            )

        try:
            new_bank = Bank(**bank_data.model_dump())
            await self.bank_repository.add_bank(new_bank)

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"message": "Bank successfully created"},
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create bank: {str(e)}",
            )

    async def delete_bank(self, swift_code: str):
        existing_bank = await self.bank_repository.get_bank_by_swift(swift_code)
        if not existing_bank:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bank with this SWIFT code doesn't exist",
            )

        await self.bank_repository.delete_bank(swift_code)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Bank successfully deleted"},
        )


def get_bank_service(
    bank_repository: BankRepository = Depends(get_bank_repository),
) -> BankService:
    return BankService(bank_repository)
