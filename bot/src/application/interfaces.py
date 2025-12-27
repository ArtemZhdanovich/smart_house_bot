import types
from typing import Any, Optional, Protocol, Self, Type  # type: ignore [attr-defined]
from uuid import UUID

from domain.entities import TelegramUserDM


class UUIDGenerator(Protocol):
    def __call__(self) -> UUID:
        ...


class SessionProtocol(Protocol):
    
    async def commit(self) -> None:
        ...
    
    async def flush(self) -> None:
        ...
    
    async def rollback(self) -> None:
        ...
    
    async def begin(self) -> None:
        ...


class TelegramUserRepositoryProtocol(Protocol):
    def __init__(self, session: SessionProtocol) -> None:
        ...

    async def add(
        self,
        user_id: UUID,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> UUID:
        ...

    async def get(
        self,
        *,
        id: UUID | None = None,
        telegram_id: int | None = None,
        username: str | None = None,
        lock: Any | None = None,
    ) -> TelegramUserDM | None:
        ...

    async def update(
        self,
        telegram_id: int,
        username: str | None,
        first_name: str | None,
        last_name: str | None,
    ) -> None:
        ...

    async def delete(self, telegram_id: int) -> None:
        ...


class UnitOfWorkProtocol(Protocol):
    users: TelegramUserRepositoryProtocol

    async def __aenter__(self) -> Self:
        ...

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[types.TracebackType],
    ) -> None: 
        ...
