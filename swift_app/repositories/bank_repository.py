from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from typing import List

from ..models.bank_model import Bank
from ..schemas.bank_schemas import BankCreate
from ..database import get_db


class BankRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_bank_by_swift(self, swift_code: str) -> Bank | None:
        return await self.db.get(Bank, swift_code)

    async def get_bank_branches(self, swift_base: str) -> List[Bank] | None:
        pattern = swift_base + "___"

        query = (
            select(Bank)
            .where(Bank.swiftCode.like(pattern))
            .where(Bank.swiftCode != swift_base + "XXX")
        )

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_banks_by_country_code(self, countryISO2: str) -> List[Bank] | None:
        query = select(Bank).where(Bank.countryISO2 == countryISO2)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def add_bank(self, bank_data: BankCreate) -> bool:
        bank = Bank(**bank_data.model_dump())
        self.db.add(bank)
        await self.db.commit()
        await self.db.refresh(bank)
        return True

    async def delete_bank(self, swift_code: str) -> bool:
        bank = await self.get_bank_by_swift(swift_code)
        if not bank:
            return False
        await self.db.delete(bank)
        await self.db.commit()
        return True


async def get_bank_repository(db: AsyncSession = Depends(get_db)) -> BankRepository:
    return BankRepository(db)
