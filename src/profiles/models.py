from sqlalchemy import Column, String, Integer, Table, Text, MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = MetaData()

profiles_table = Table(
    "profiles",
    metadata,
    Column("email", String(), primary_key=True, nullable=False),
    Column("name", String(), nullable=False),
    Column("age", Integer(), nullable=False),
    Column("description", Text()),
    Column("hobbies", Text()),
    Column("preferences", Text()),
    Column("location", String(), nullable=False),
    Column("contacts", String(), nullable=False)
)


class Profile(Base):
    __tablename__ = "profiles"
    email = Column("email", String(), primary_key=True, nullable=False)
    name = Column("name", String(), nullable=False)
    age = Column("age", Integer(), nullable=False)
    description = Column("description", Text())
    hobbies = Column("hobbies", Text())
    preferences = Column("preferences", Text())
    location = Column("location", String(), nullable=False)
    contacts = Column("contacts", String(), nullable=False)
