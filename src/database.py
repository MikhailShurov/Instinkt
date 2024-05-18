import datetime

from sqlalchemy import select, insert, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import user_table, Users
from src.profiles.models import profiles_table, Profile
from src.profiles.schemas import NewProfileInfo
from src.likes.models import likes


class DBManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, email: str, hashed_password: str):
        try:
            user = Users(email=email, hashed_password=hashed_password, account_created=str(datetime.datetime.utcnow()))
            self.session.add(user)
            await self.session.commit()
            return user.id
        except Exception as e:
            return {"success": False, "message": str(e)}

    async def get_user_by_email(self, email: str):
        query = select(user_table).where(user_table.c.email == email)
        result = await self.session.execute(query)
        user = result.fetchone()
        await self.session.commit()
        return user

    async def get_profile_by_id(self, user_id: int):
        query = select(profiles_table).where(profiles_table.c.id == user_id)
        result = await self.session.execute(query)
        profile = result.fetchone()
        await self.session.commit()
        return profile

    async def get_location_by_id(self, user_id: int):
        query = select(profiles_table.c.location).where(profiles_table.c.id == user_id)
        result = await self.session.execute(query)
        location = result.scalar()
        await self.session.commit()
        return location

    async def check_if_like_exists(self, user_id: int):
        query = select(exists().where(likes.c.sender_id == user_id))
        result = await self.session.execute(query)
        return result.scalar()

    async def update_profile_info(self, user_id: int, new_profile_info: NewProfileInfo):
        profile_dict = new_profile_info.dict()
        update_fields = {"name": profile_dict["name"], "age": profile_dict["age"],
                         "description": profile_dict["description"], "hobbies": profile_dict["hobbies"],
                         "preferences": profile_dict["preferences"], "location": profile_dict["location"],
                         "contacts": profile_dict["contacts"]}

        query = profiles_table.update().where(profiles_table.c.id == user_id).values(update_fields)
        await self.session.execute(query)
        await self.session.commit()

    async def update_prime_status(self, uid: int, prime: bool):
        query = user_table.update().where(user_table.c.id == uid).values(prime_status=prime)
        await self.session.execute(query)
        await self.session.commit()

    async def get_user_location(self, user_id: int):
        queue = select(profiles_table.c.location).where(profiles_table.c.id == user_id)
        result = await self.session.execute(queue)
        await self.session.commit()
        return result.scalar()

    async def check_prime_status(self, uid: int):
        query = select(user_table.c.prime_status).where(user_table.c.id == uid)
        result = await self.session.execute(query)
        await self.session.commit()
        prime_status = result.scalar()
        return prime_status

    async def like(self, sender_id: int, receiver_id: int):
        values = {
            'sender_id': sender_id,
            'receiver_id': receiver_id
        }
        try:
            query = insert(likes).values(values)
            await self.session.execute(query)
            await self.session.commit()
        except Exception as _:
            await self.session.commit()
            raise Exception("Like already exists")
        return {"like_status": "ok"}
        # return {"like_status": "like is akready exists"}

    async def get_mutual_likes(self, uid: int):
        query = select(likes).where(
            likes.c.sender_id == uid
        )
        result = await self.session.execute(query)
        records = result.fetchall()

        query2 = select(likes).where(
            likes.c.receiver_id == uid
        )
        tmp = await self.session.execute(query2)
        tmp = tmp.fetchall()

        await self.session.commit()

        result2 = [(like[1], like[0]) for like in tmp]
        result = [like for like in result2 if like in records]
        return result

    async def create_empty_profile(self, email: str):
        try:
            d_description = "Some words about yourself"
            d_hobbies = "Your hobbies"
            d_preferences = "false,false,false,false,false"
            d_location = "0.00000, 0.00000"
            d_contacts = "Place your contacts here:)"
            profile = Profile(email=email, name="Name", age=0, description=d_description, hobbies=d_hobbies,
                              preferences=d_preferences, location=d_location, contacts=d_contacts)

            self.session.add(profile)
            await self.session.commit()
        except Exception as e:
            return {"success": False, "message": str(e)}
