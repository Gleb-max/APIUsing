import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Job(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "jobs"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    leader = orm.relation("User")
    job = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.datetime.now, nullable=True)
    end_date = sqlalchemy.Column(sqlalchemy.Date, nullable=True)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    # def __str__(self):
    #     return f"<Job> id: {self.id} team_leader: [{self.leader}] job: {self.job}"
    #
    # def __repr__(self):
    #     return self.__str__()
