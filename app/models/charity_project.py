from sqlalchemy import Column, String, Text

from .generalmodel import GeneralModel


class CharityProject(GeneralModel):
    '''
    Модель проектов.
    Унаследована от GeneralModel.
    '''

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
