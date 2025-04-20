from pydantic import BaseModel, Field


class BankCreate(BaseModel):
    address: str = Field()
    bankName: str = Field()
    countryISO2: str = Field()
    countryName: str = Field()
    isHeadquarter: bool = Field()
    swiftCode: str = Field()
