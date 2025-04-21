from sqlmodel import SQLModel, Field
from typing import List


class BankCreate(SQLModel):
    address: str
    bankName: str
    countryISO2: str
    countryName: str
    isHeadquarter: bool
    swiftCode: str


class BasicBankResponse(SQLModel):
    address: str
    bankName: str
    countryISO2: str
    isHeadquarter: bool
    swiftCode: str

    class Config:
        orm_mode = True


class DetailedBankResponse(SQLModel):
    address: str
    bankName: str
    countryISO2: str
    countryName: str
    isHeadquarter: bool
    swiftCode: str
    branches: List[BasicBankResponse] = Field(default_factory=list)

    class Config:
        orm_mode = True


class CountryBankResponse(SQLModel):
    countryISO2: str
    countryName: str
    swiftCodes: List[BasicBankResponse] = Field(default_factory=list)

    class Config:
        orm_mode = True
