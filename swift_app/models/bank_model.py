from sqlmodel import SQLModel, Field


class Bank(SQLModel, table=True):
    __tablename__ = "banks"

    swiftCode: str = Field(primary_key=True, index=True)
    address: str = Field(nullable=True)
    bankName: str = Field(nullable=False)
    countryISO2: str = Field(nullable=False)
    countryName: str = Field(nullable=False)
    isHeadquarter: bool = Field(nullable=False)
