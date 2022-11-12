from typing import List
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.schemas.charityproject import CharityProjectDB


FORMAT = '%Y/%m/%d %H:%M:%S'

# Настройки google
DRIVE_VERSION = 'v3'
SHEETS_VERSION = 'v4'

# Настройки таблицы
TABLE_LOCALE = 'ru_RU'

# Настройки первого листа
TABLE_FIRST_SHEET__SHEET_TYPE = 'GRID'
TABLE_FIRST_SHEET__SHEET_ID = 0
TABLE_FIRST_SHEET__TITLE = 'Лист1'
TABLE_FIRST_SHEET__ROW_COUNT = 100
TABLE_FIRST_SHEET__COLUMN_COUNT = 11


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    """Предоставляем права доступа."""
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', DRIVE_VERSION)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создаем таблицу."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', SHEETS_VERSION)

    spreadsheet_body = {
        'properties': {
            'title': f'Отчет на {now_date_time}',
            'locale': TABLE_LOCALE},
        'sheets': [{'properties': {
            'sheetType': TABLE_FIRST_SHEET__SHEET_TYPE,
            'sheetId': TABLE_FIRST_SHEET__SHEET_ID,
            'title': TABLE_FIRST_SHEET__TITLE,
            'gridProperties': {
                'rowCount': TABLE_FIRST_SHEET__ROW_COUNT,
                'columnCount': TABLE_FIRST_SHEET__COLUMN_COUNT}}}]
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

    service = await wrapper_services.discover('sheets', SHEETS_VERSION)
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
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'A1:C{values_in_table}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
