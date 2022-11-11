from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charityproject import charity_project_crud
from app.crud.donations import donation_crud
from app.models.user import User
from app.schemas.donations import DonationCreate, DonationDB, DonationUser
from app.services.investing import investing_function


router = APIRouter()


@router.post(
    '/',
    response_model=DonationUser,
    response_model_exclude_none=True
)
async def create_donation(
        new_donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
) -> DonationUser:
    '''Только для зарегистрированных пользователей.
    Создаёт пожертвование.
    '''
    donation = await donation_crud.create(new_donation, session, user)
    await investing_function(
        first_obj=charity_project_crud,
        second_obj=donation,
        session=session
    )
    return donation


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    '''Получение списка всех пожертований.'''
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=List[DonationUser]
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    '''Получение списка пожертвований пользователя.'''
    return await donation_crud.get_by_user(session, user)
