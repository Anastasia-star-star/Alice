import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Genres(SqlAlchemyBase):
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    # start Блок, отвечающий за столбцы таблицы
    id_film = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("films.id"))
    id_genre = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("genre.id"))
    # end

    f = orm.relation('Films')
    g = orm.relation('Genre')