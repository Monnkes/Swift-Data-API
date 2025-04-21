from sqlmodel import SQLModel, Field
from pydantic import ConfigDict, field_validator, model_validator
from typing import List


class BankCreate(SQLModel):
    address: str
    bankName: str
    countryISO2: str
    countryName: str
    isHeadquarter: bool
    swiftCode: str

    @field_validator("swiftCode")
    def validate_swift_code(cls, v):
        if len(v) != 11:
            raise ValueError("SWIFT code must be exactly 11 characters long")
        if not v.isupper() or not v.isalnum():
            raise ValueError("SWIFT code must be uppercase alphanumeric")
        return v

    @field_validator("countryISO2")
    def validate_country_iso(cls, v):
        if len(v) != 2 or not v.isalpha() or not v.isupper():
            raise ValueError("Country code must be 2 uppercase letters")
        return v

    @field_validator("countryName")
    def validate_country_name(cls, v):
        if not v.isupper() or any(char.isdigit() for char in v):
            raise ValueError("Country name must be uppercase letters")
        return v

    @model_validator(mode="after")
    def validate_headquarter(self):
        if self.isHeadquarter and not self.swiftCode.endswith("XXX"):
            raise ValueError("Headquarter must have XXX as last 3 characters")
        if not self.isHeadquarter and self.swiftCode.endswith("XXX"):
            raise ValueError("Branch must not have XXX as last 3 characters")
        return self


class BasicBankResponse(SQLModel):
    address: str
    bankName: str
    countryISO2: str
    isHeadquarter: bool
    swiftCode: str

    model_config = ConfigDict(from_attributes=True)


class DetailedBankResponse(SQLModel):
    address: str
    bankName: str
    countryISO2: str
    countryName: str
    isHeadquarter: bool
    swiftCode: str
    branches: List[BasicBankResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class CountryBankResponse(SQLModel):
    countryISO2: str
    countryName: str
    swiftCodes: List[BasicBankResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
