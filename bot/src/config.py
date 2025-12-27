import os

from pydantic import BaseModel, Field


class RabbitMQConfig(BaseModel):
    host: str = Field(alias="MQ_HOST")
    port: int = Field(alias="MQ_PORT")
    login: str = Field(alias="MQ_USER")
    password: str = Field(alias="MQ_PASS")
    vhost: str = Field(alias="MQ_VHOST")


class RedisConfig(BaseModel):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT")
    db: int = Field(alias="REDIS_DB")
    password: str = Field(alias="REDIS_PASS")


class PostgresConfig(BaseModel):
    host: str = Field(alias="DB_HOST")
    port: int = Field(alias="DB_PORT")
    login: str = Field(alias="DB_USER")
    password: str = Field(alias="DB_PASS")
    database: str = Field(alias="DB_NAME")


class BotConfig(BaseModel):
    token: str = Field(alias="BOT_TOKEN")


class Config(BaseModel):
    rabbit: RabbitMQConfig = Field(
        default_factory=lambda: RabbitMQConfig.model_validate(os.environ)
    )
    redis: RedisConfig = Field(
        default_factory=lambda: RedisConfig.model_validate(os.environ)
    )
    bot: BotConfig = Field(
        default_factory=lambda: BotConfig.model_validate(os.environ)
    )
    postgres: PostgresConfig = Field(
        default_factory=lambda: PostgresConfig.model_validate(os.environ)
    )