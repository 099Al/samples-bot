from sqlalchemy import select

from database.connect import DataBase
from database.models import T_A


class ReqA:
    def __init__(self):
        self.session = DataBase().get_session()



    async def get_a(self, id):
        async with self.session() as session:
            result = await session.execute(
                select(T_A).where(T_A.id == id)
            )
            return result.scalars().one_or_none()


    async def get_desc(self, id):
        async with self.session() as session:
            a = await session.get(T_A, id)
            desc = a.r_desc

            return desc.scalars().all()