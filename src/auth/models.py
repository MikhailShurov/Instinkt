import sqlalchemy
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean, Integer, DateTime
from sqlalchemy.orm import mapped_column
from src.database import Base

metadata = sqlalchemy.MetaData()

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(), unique=True, index=True),
    sqlalchemy.Column("hashed_password", sqlalchemy.String()),
    sqlalchemy.Column("account_created", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("is_superuser", sqlalchemy.Boolean),
    sqlalchemy.Column("is_verified", sqlalchemy.Boolean)
)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    id = sqlalchemy.Column(Integer, primary_key=True)
    email = sqlalchemy.Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password = sqlalchemy.Column(String(length=1024), nullable=False)
    account_created = sqlalchemy.Column(DateTime, nullable=False)
    is_active = sqlalchemy.Column(Boolean, default=True, nullable=False)
    is_superuser = sqlalchemy.Column(Boolean, default=False, nullable=False)
    is_verified = sqlalchemy.Column(Boolean, default=False, nullable=False)
