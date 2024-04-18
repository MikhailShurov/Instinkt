import sqlalchemy
from sqlalchemy import String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

metadata = sqlalchemy.MetaData()

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("email", sqlalchemy.String(), unique=True, index=True, primary_key=True),
    sqlalchemy.Column("hashed_password", sqlalchemy.String()),
    sqlalchemy.Column("account_created", sqlalchemy.String(), nullable=False),
)


class Users(Base):
    __tablename__ = "users"
    email = sqlalchemy.Column(String(length=320), unique=True, index=True, nullable=False, primary_key=True)
    hashed_password = sqlalchemy.Column(String(length=1024), nullable=False)
    account_created = sqlalchemy.Column(String(length=100), nullable=False)
