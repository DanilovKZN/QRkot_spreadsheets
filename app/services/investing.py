from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession


def close_project_or_donat(objects) -> None:
    '''Закрывает сбор средств или
    свободный остаток доната
    '''
    for object in objects:
        if object.full_amount == object.invested_amount:
            object.fully_invested = True
            object.close_date = datetime.now()


async def investing_function(
    first_obj,
    second_obj,
    session: AsyncSession
):
    """Реализация инвестирования по ТЗ."""
    # Ищем незакрытые проеты / свободные донаты
    objects = await first_obj.get_not_closed_objects(session)
    for object in objects:
        # Сколько имеем
        have_investing = object.full_amount - object.invested_amount
        # Сколько нужно
        need_investing = second_obj.full_amount - second_obj.invested_amount
        # Часть или всё
        if have_investing > need_investing:
            investing = need_investing
        else:
            investing = have_investing
        object.invested_amount += investing
        second_obj.invested_amount += investing
        close_project_or_donat([object, second_obj])

    session.add_all((*objects, second_obj))
    await session.commit()
    await session.refresh(second_obj)
    return second_obj
