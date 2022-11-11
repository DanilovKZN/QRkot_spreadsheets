# QRkot_spreadseets

## Коротко о проекте

   Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.
    В приложение QRKot добавлена возможность формирования отчёта в гугл-таблицу. Туда заносятся закрытые проекты, отсортированные по скорости сбора средств — от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.

## Как запустить проект:


Клонировать репозиторий и перейти в него в командной строке:


```

git clone https://github.com/DanilovKZN/QRkot_spreadsheets.git

```

  

```

cd cat_charity_fund

```

  

Cоздать и активировать виртуальное окружение:

  

```

python3 -m venv venv

```

  

* Если у вас Linux/MacOS

  

```

source venv/bin/activate

```

  

* Если у вас windows

  

```

source venv/scripts/activate

```

  

Установить зависимости из файла requirements.txt:

  

```

python3 -m pip install --upgrade pip

```
Отредактировать файл `.env`  :
```

APP_TITLE=QRKot
DESCRIPTION=Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.
DATABASE_URL=ваша БД(Пример: sqlite+aiosqlite:///./название_БД.db)
SECRET=Любое секретное слово — ключ для хеширования пароля
FIRST_SUPERUSER_EMAIL='Мыло' админа
FIRST_SUPERUSER_PASSWORD=Пароль админа

Далее идет информация из полученного JSON-файл с ключом доступа к сервисному аккаунту

TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
EMAIL=

```

Создать и применить миграции:

```
alembic revision --autogenerate -m "Название миграции"

alembic upgrade head


```
Запустить проект:


```

uvicorn app.main:app --reload


```
Документация проекта:

```
http://127.0.0.1:8000/docs
```

12. Технологии:

```
Alembic
FastAPI
FastAPI Users
Google Drive API
Google Sheets API
Python
SQLAlchemy

```
13. Автор:
```
Данилов Николай