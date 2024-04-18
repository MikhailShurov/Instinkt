import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import user_table, Users


class DBManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, email: str, hashed_password: str):
        try:
            user = Users(email=email, hashed_password=hashed_password, account_created=str(datetime.datetime))
            self.session.add(user)
            await self.session.commit()
            return {"success": True, "message": "User created successfully", "user": user}
        except Exception as e:
            return {"success": False, "message": str(e)}

    async def get_user_by_email(self, email: str):
        query = select(user_table).where(user_table.c.email == email)
        result = await self.session.execute(query)
        user = result.fetchone()
        return user
