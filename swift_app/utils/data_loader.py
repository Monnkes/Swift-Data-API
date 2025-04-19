import pandas as pd
from sqlalchemy.orm import Session

from swift_app.models.bank_model import Bank
from swift_app.settings import config
from swift_app.data.column_mapping import COLUMN_MAPPING


def load_initial_data(db: Session):
    if db.query(Bank).count() > 0:
        return

    df = pd.read_excel(config.SWIFT_DATA_URL)
    df = df.drop(["CODE TYPE", "TOWN NAME", "TIME ZONE"], axis=1)
    df = df.rename(columns=COLUMN_MAPPING)
    records = df.to_dict(orient="records")
    bank_objects = [Bank(**record) for record in records]

    db.bulk_save_objects(bank_objects)
    db.commit()
