from types import TracebackType
from typing import Self, Type  # type: ignore [attr-defined]

from application.interfaces import SessionProtocol, TelegramUserRepositoryProtocol


class UnitOfWork:
    def __init__(
        self, 
        session: SessionProtocol, 
        users: type[TelegramUserRepositoryProtocol]
    ) -> None:
        self._session = session
        self._users = users(session)

    async def __aenter__(self) -> Self:
        await self._session.begin()
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()
