import sqlalchemy

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