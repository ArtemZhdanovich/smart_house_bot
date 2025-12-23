from typing import Any, AsyncIterable

from config import Config
from dishka import Provider, Scope, from_context, provide
from faststream.rabbit import RabbitBroker
from infrastructure.redis import new_redis_client
from redis.asyncio import Redis


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    broker = from_context(provides=RabbitBroker, scope=Scope.APP)

    @provide(scope=Scope.REQUEST)
    async def get_redis_conn(self, config: Config) -> AsyncIterable[Redis[Any]]:
        conn = new_redis_client(config.redis)
        try:
            yield conn
        finally:
            await conn.close()