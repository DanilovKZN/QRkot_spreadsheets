from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charityproject import CharityProjectUpdate


SAME_NAME_PROJECT = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUNDED = 'Проект не найден!'
PROJECT_ALREADY_CLOSED = 'Закрытый проект нельзя редактировать!'
NOT_SUPERUSER = 'Доступно только суперюзеру.'
BAD_FULL_AMOUNT = 'Требуемая сумма не может быть меньше уже внесённой!'
PROJECT_ALREADY_INVESTED = 'В проект были внесены средства, не подлежит удалению!'


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    '''Проверка на уникальность.'''
    project_name = await charity_project_crud.get_project_by_name(project_name, session)
    if project_name is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=SAME_NAME_PROJECT
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    '''Проверка на наличие проекта.'''
    charity_project = await charity_project_crud.get(project_id, session)
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUNDED
        )
    return charity_project


async def check_project_before_update(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession
) -> CharityProject:
    """Проверка перед обновлением проекта."""
    project = await charity_project_crud.get(project_id, session)

    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUNDED
        )

    if obj_in.name and obj_in.name != project.name:
        await check_name_duplicate(obj_in.name, session)

    if project.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_ALREADY_CLOSED
        )

    if obj_in.full_amount and obj_in.full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=BAD_FULL_AMOUNT
        )

    return project


async def check_project_already_invested(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    '''Проверка перед удалением на наличие внесений.'''
    await check_project_exists(project_id, session)
    project = await charity_project_crud.get(project_id, session)

    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_ALREADY_INVESTED
        )

    return project
