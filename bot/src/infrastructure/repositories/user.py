import uuid

from sqlalchemy import RowMapping, text
from sqlalchemy.ext.asyncio import AsyncSession


class TelegramUserRepositorySQL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(
        self, 
        telegram_id: int, 
        username: str | None = None,
        first_name: str | None = None, 
        last_name: str | None = None
    ) -> uuid.UUID:
        user_id = uuid.uuid4()
        stmt = text("""
            INSERT INTO telegram_users (
                id,
                telegram_id, 
                username, 
                first_name, 
                last_name
            )
            VALUES (
                :id, 
                :telegram_id, 
                :username, 
                :first_name, 
                :last_name
            )
        """)
        await self.session.execute(stmt, {
            "id": user_id,
            "telegram_id": telegram_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        })
        await self.session.commit()
        return user_id

    async def get(
        self,
        *, 
        id: uuid.UUID | None = None,
        telegram_id: int | None = None,
        username: str | None = None
    ) -> RowMapping | None:
        if id is not None:
            stmt = text("""
                SELECT * FROM telegram_users 
                WHERE id = :id
            """)
            result = await self.session.execute(stmt, {"id": id})
            return result.mappings().first()
        if telegram_id is not None:
            stmt = text("""
                SELECT * FROM telegram_users 
                WHERE telegram_id = :telegram_id
            """)
            result = await self.session.execute(stmt, {"telegram_id": telegram_id})
            return result.mappings().first()
        if username is not None:
            stmt = text("""
                SELECT * FROM telegram_users 
                WHERE username = :username
            """)
            result = await self.session.execute(stmt, {"username": username})
            return result.mappings().first()
        raise ValueError("Нужно указать хотя бы один уникальный ключ")

    async def update_user_info(
        self, 
        telegram_id: int, 
        username: str | None, 
        first_name: str | None, 
        last_name: str | None
    ) -> None:
        stmt = text("""
            UPDATE telegram_users
            SET username = :username,
                first_name = :first_name,
                last_name = :last_name
            WHERE telegram_id = :telegram_id
        """)
        await self.session.execute(
            stmt,
            {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "telegram_id": telegram_id,
            }
        )
        await self.session.commit()

    async def delete(self, telegram_id: int) -> None:
        stmt = text("""
            DELETE FROM telegram_users 
            WHERE telegram_id = :telegram_id
        """)
        await self.session.execute(stmt, {"telegram_id": telegram_id})
        await self.session.commit()
