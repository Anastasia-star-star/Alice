import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Genre(SqlAlchemyBase):
    __tablename__ = 'genre'

    # start Блок, отвечающий за столбцы таблицы
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title_g = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # end

    genres = orm.relation("Genres", back_populates='g')


