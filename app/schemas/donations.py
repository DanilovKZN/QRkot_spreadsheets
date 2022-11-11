from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt = Field(..., title='Необходимая сумма')
    comment: Optional[str] = Field(None, title='Комментарий')

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationUser(DonationBase):
    id: int
    create_date: datetime = Field(..., title='Дата пожертвования')

    class Config:
        orm_mode = True


class DonationDB(DonationUser):
    user_id: int
    invested_amount: int = Field(..., title='Сумма распределённая по проектам')
    fully_invested: bool = Field(..., title='Переведена ли вся сумма в проекты')
    close_date: Optional[datetime] = Field(None, title='Дата распределения пожертвования')
