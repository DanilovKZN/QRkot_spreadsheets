from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_project_already_invested,
    check_project_before_update,
    check_project_exists
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.crud.donations import donation_crud
from app.schemas.charityproject import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.investing import investing_function


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    '''
    Создание проекта.
    Доступно только суперпользователю.
    '''
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    await investing_function(
        first_obj=donation_crud,
        second_obj=new_project,
        session=session
    )
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session)
):
    '''Получение всех проектов.'''
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    '''
    Обновление проекта.
    Доступно только суперпользователю.
    '''
    await check_project_exists(project_id, session)
    project = await check_project_before_update(project_id, obj_in, session)
    return await charity_project_crud.update(
        project,
        obj_in,
        session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    '''
    Удаление проекта.
    Доступно только суперпользователю,
    при отсутсвии зачислений.
    '''
    project = await check_project_already_invested(project_id, session)
    return await charity_project_crud.remove(project, session)
