import datetime

import sqlalchemy

from db_Illustrator_master.db_session_master import SqlAlchemyBase


class Main_master(SqlAlchemyBase):
    __tablename__ = 'main_db_Illustrator_master'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    drawing = sqlalchemy.Column(sqlalchemy.String(100), unique=True)

    def __repr__(self):
        return [(self.id, self.time, self.drawing)]
