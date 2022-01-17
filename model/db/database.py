import datetime

from sqlalchemy import create_engine, MetaData, Column, Integer, String, DateTime, ForeignKey, Boolean, Float
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
    is_admin = Column(Boolean, nullable=False, default=False)

    subjects = relationship('Subject', secondary='user_has_subject')

    def __init__(self, first_name: str, surname: str, dob: datetime, email: str, password: str, is_admin=False):
        user = vc.User(first_name, surname, dob, email, password, is_admin)

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
               f"password={self.password}, " \
               f"is_admin={self.is_admin}" \
               f")>"


class Subject(Base):
    """Subject table"""
    __tablename__ = 'subjects'
    subject_id = Column(Integer, primary_key=True, autoincrement=True)
    subject_code = Column(String(100), nullable=False)
    subject_name = Column(String(100), nullable=True)
    credits = Column(Float, nullable=True)

    def __init__(self, subject_code: str, subject_name: str, credits: float):
        subject = vc.Subject(subject_code, subject_name, credits)
        self.subject_code = subject.get_subject_code()
        self.subject_name = subject.get_subject_name()
        self.credits = subject.get_credits()

    def __repr__(self):
        return f"<Subject(" \
               f"subject_id={self.subject_id}, " \
               f"subject_code={self.subject_code}, " \
               f"subject_name={self.subject_name}, " \
               f"credits={self.credits}" \
               f")>"


class UserHasSubject(Base):
    __tablename__ = 'user_has_subject'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), primary_key=True)
    grade_id = Column(Integer, ForeignKey('grades.grade_id'), nullable=True)
    exam_date = Column(DateTime, nullable=True)

    def __init__(self, user_id: int, subject_id: int, grade_id=1, exam_date=None):
        self.user_id = user_id
        self.subject_id = subject_id
        self.grade_id = grade_id
        self.exam_date = exam_date  # No need for validation, because exam date can be in the future or the past. It
        # can also be null/none


class Grade(Base):
    __tablename__ = 'grades'
    grade_id = Column(Integer, primary_key=True, autoincrement=True)
    grade_value = Column(String(100), nullable=False)

    user_subjects = relationship('UserHasSubject', backref='user_has_subject')

    def __init__(self, grade_value: str):
        if not isinstance(grade_value, str):
            raise TypeError("Invalid datatype fore grade value.")

        self.grade_value = grade_value

    def __repr__(self):
        return f"<Grade(" \
               f"grade_id={self.grade_id}, " \
               f"grade_value={self.grade_value}" \
               f")>"


def init_db():
    Base.metadata.create_all(bind=engine)

    # Creating data that program needs to run. There is no way to change this within the program
    # Grades
    """
    ongoing = Grade('Ongoing')
    a = Grade('A')
    b = Grade('B')
    c = Grade('C')
    d = Grade('D')
    e = Grade('E')
    passed = Grade('Pass')
    fail = Grade('Fail')

    session.add_all([ongoing, a, b, c, d, e, passed, fail])
    session.commit()
    """

