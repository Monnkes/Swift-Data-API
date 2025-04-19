import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.bank_model import Bank
from ..settings import config
from ..data.column_mapping import COLUMN_MAPPING


async def load_initial_data(db: AsyncSession):
    result = await db.execute(select(Bank))
    if result.scalars().first() is not None:
        return

    df = pd.read_excel(config.SWIFT_DATA_URL)
    df = df.drop(["CODE TYPE", "TOWN NAME", "TIME ZONE"], axis=1)
    df = df.rename(columns=COLUMN_MAPPING)
    df["isHeadquarter"] = df["swiftCode"].str[-3:] == "XXX"
    records = df.to_dict(orient="records")
    bank_objects = [Bank(**record) for record in records]

    db.add_all(bank_objects)
    await db.commit()
