from sqlalchemy import Column, ForeignKey, Integer, Text

from .generalmodel import GeneralModel


class Donation(GeneralModel):
    '''
    Модель пожертований.
    Унаследована от GeneralModel.
    '''

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
