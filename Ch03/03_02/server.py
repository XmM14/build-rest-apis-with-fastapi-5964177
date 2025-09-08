from datetime import datetime
from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import db

app = FastAPI()


class Sale(BaseModel):
    time: datetime
    customer_id: str = Field(min_length=2)
    sku: str = Field(min_length=2)
    amount: int = Field(gt=0)
    price: float = Field(gt=0)  # $


@app.post('/sales/')
def new_sale(sale: Sale):
    record = db.Sale(
        time=sale.time,
        sku=sale.sku,
        customer_id=sale.customer_id,
        amount=sale.amount,
        price=int(sale.price * 100),
    )
    key = db.insert(record)
    return {
        'key': key,
    }


@app.get('/sales/{key}')
def get_sale(key: str) -> Sale:
    if not key or not db.isValidKey(key):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail='Invalid sale key')

    record = db.get(key)
    if record is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='sale not found')

    s = Sale(
        time=record.time,
        sku=record.sku,
        customer_id=record.customer_id,
        amount=record.amount,
        price=record.price / 100,
    )
    return s
