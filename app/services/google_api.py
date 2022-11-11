from typing import List
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.schemas.charityproject import CharityProjectDB


FORMAT = "%Y/%m/%d %H:%M:%S"


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    """Предоставляем права доступа."""
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создаем таблицу."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    spreadsheet_body = {
        'properties': {
            'title': f'Отчет на {now_date_time}',
            'locale': 'ru_RU'},
        'sheets': [{'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Лист1',
            'gridProperties': {
                'rowCount': 100,
                'columnCount': 11}}}]
    }

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def spreadsheets_update_value(
        spreadsheetid: str,
        charity_projects: List[CharityProjectDB],
        wrapper_services: Aiogoogle
) -> None:
    """Создаём/Обновляем поля таблицы."""
    now_date_time = datetime.now().strftime(FORMAT)

    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    for project in charity_projects:
        collection_time = project.close_date - project.create_date
        new_row = [
            str(project.name),
            str(collection_time),
            str(project.description)
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    values_in_table = str(len(table_values))
    response = await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'A1:C{values_in_table}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )