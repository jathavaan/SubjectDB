import datetime

from sqlalchemy import create_engine, MetaData, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

import model.validation_classes as vc

engine = create_engine(
    'sqlite:///subjectDB',
    connect_args={'check_same_thread': False},
    echo=True
)

session = sessionmaker(autoflush=True, bind=engine)()

metadata = MetaData(
    naming_convention={
        "ix": "ix__%(column_0_label)s",
        "uq": "uq__%(table_name)s__%(column_0_name)s",
        "ck": "ck__%(table_name)s__%(constraint_name)s",
        "fk": "fk__%(table_name)s__%(column_0_name)s__%(referred_table_name)s",
        "pk": "pk__%(table_name)s"
    }
)

Base = declarative_base(metadata=metadata)


class User(Base):
    """User table"""
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    dob = Column(DateTime, nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    subjects = relationship('Subject', secondary='user_has_subject')

    def __init__(self, first_name: str, surname: str, dob: datetime, email: str, password: str):
        user = vc.User(first_name, surname, dob, email, password)

        self.first_name = user.get_first_name()
        self.surname = user.get_surname()
        self.dob = user.get_dob()
        self.email = user.get_email()
        self.password = user.get_password()

    def __repr__(self):
        return f"<User(" \
               f"user_id={self.user_id}, " \
               f"first_name={self.first_name}, " \
               f"surname={self.surname}, " \
               f"dob={self.dob}, " \
               f"email={self.email}, " \
               f"password={self.password}" \
               f")>"


class Subject(Base):
    """Subject table"""
    __tablename__ = 'subjects'
    subject_id = Column(Integer, primary_key=True, autoincrement=True)
    subject_code = Column(String(100), nullable=False)
    subject_name = Column(String(100), nullable=True)

    # users = relationship('User', secondary='user_has_subject')

    def __init__(self, subject_code: str, subject_name: str):
        subject = vc.Subject(subject_code, subject_name)
        self.subject_code = subject.get_subject_code()
        self.subject_name = subject.get_subject_name()

    def __repr__(self):
        return f"<Subject(" \
               f"subject_id={self.subject_id}, " \
               f"subject_code={self.subject_code}, " \
               f"subject_name={self.subject_name}" \
               f")>"


class UserHasSubject(Base):
    __tablename__ = 'user_has_subject'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), primary_key=True)

    def __init__(self, user_id: int, subject_id: int):
        self.user_id = user_id
        self.subject_id = subject_id


def init_db():
    Base.metadata.create_all(bind=engine)


init_db()