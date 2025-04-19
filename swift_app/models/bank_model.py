from sqlalchemy import Column, String, Boolean

from swift_app.databse import Base


class Bank(Base):
    __tablename__ = "banks"

    swiftCode = Column(String, primary_key=True, index=True)
    address = Column(String, nullable=True)
    bankName = Column(String, nullable=False)
    countryISO2 = Column(String, nullable=False, index=True)
    countryName = Column(String, nullable=False)
    isHeadquarter = Column(Boolean, nullable=False)
