import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import user_table, Users
from src.profiles.models import profiles_table, Profile


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
        await self.session.commit()
        return user

    async def get_profile_by_email(self, email: str):
        query = select(profiles_table).where(profiles_table.c.email == email)
        result = await self.session.execute(query)
        profile = result.fetchone()
        await self.session.commit()
        return profile

    async def update_profile_info(self, new_profile_info: Profile):
        profile_dict = new_profile_info.dict()
        query = profiles_table.update().where(profiles_table.c.email == new_profile_info.email).values(profile_dict)
        await self.session.execute(query)
        await self.session.commit()

    async def create_empty_profile(self, email: str):
        try:
            d_description = "Some words about yourself"
            d_hobbies = "Your hobbies"
            d_preferences = "Tell about your favourite music/books/games"
            d_location = "Your location"
            d_contacts = "Place your contacts here:)"
            profile = Profile(email=email, name="Name", age=0, description=d_description, hobbies=d_hobbies,
                              preferences=d_preferences, location=d_location, contacts=d_contacts)

            self.session.add(profile)
            await self.session.commit()
        except Exception as e:
            return {"success": False, "message": str(e)}
