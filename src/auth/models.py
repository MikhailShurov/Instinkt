from sqlalchemy import String, Column, Table, MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("email", String(), index=True, primary_key=True),
    Column("hashed_password", String()),
    Column("account_created", String(), nullable=False),
)


class Users(Base):
    __tablename__ = "users"
    email = Column(String(length=320), index=True, nullable=False, primary_key=True)
    hashed_password = Column(String(length=1024), nullable=False)
    account_created = Column(String(length=100), nullable=False)
