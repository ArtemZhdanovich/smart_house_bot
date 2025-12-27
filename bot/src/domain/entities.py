from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class TelegramUserDM:
    id: UUID
    telegram_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
