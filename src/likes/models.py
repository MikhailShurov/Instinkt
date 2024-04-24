from sqlalchemy import Column, String, Integer, Table, Text, MetaData, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = MetaData()


class Likes(Base):
    __tablename__ = "likes"
    uid = Column("sender_id", Integer(), nullable=False)
    likes = Column("receiver_id", Integer(), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('sender_id', 'receiver_id'),
    )


likes = Table(
    "likes",
    metadata,
    Column("sender_id", Integer(), nullable=False),
    Column("receiver_id", Integer(), nullable=False)
)
