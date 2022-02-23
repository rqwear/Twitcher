import contextlib
from typing import Optional, AsyncIterator
import asyncpg

from data import config


class Database:
    def __init__(self):
        self._pool: Optional[asyncpg.Pool] = None

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        full_name varchar(255) NOT NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        username varchar(255) NULL,
        is_group int DEFAULT 0,
        group_name BIGINT DEFAULT NULL,
        twitch_name varchar(255) DEFAULT NULL,
        manual_activation int DEFAULT 0,
        activation int DEFAULT 0
        );
        """
        await self.execute(sql, execute=True)
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users"
        return await self.execute(sql, fetchval=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

    async def delete_users(self):
        await self.execute("DELETE FROM users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE IF EXISTS users", execute=True)

    #update data:
    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def update_is_group(self, is_group, telegram_id):
        sql = "UPDATE users SET is_group=$1 WHERE telegram_id=$2"
        return await self.execute(sql, is_group, telegram_id, execute=True)

    async def update_twitch_name(self, twitch_name, telegram_id):
        sql = "UPDATE users SET twitch_name=$1 WHERE telegram_id=$2"
        return await self.execute(sql, twitch_name, telegram_id, execute=True)

    async def update_activation(self, activation, telegram_id):
        sql = "UPDATE users SET activation=$1 WHERE telegram_id=$2"
        return await self.execute(sql, activation, telegram_id, execute=True)

    async def update_manual_activation(self, manual_activation, telegram_id):
        sql = "UPDATE users SET manual_activation=$1 WHERE telegram_id=$2"
        return await self.execute(sql, manual_activation, telegram_id, execute=True)

    async def update_group_name(self, group_name, telegram_id):
        sql = "UPDATE users SET group_name=$1 WHERE telegram_id=$2"
        return await self.execute(sql, group_name, telegram_id, execute=True)


    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self._transaction() as connection:  # type: asyncpg.Connection
            if fetch:
                result = await connection.fetch(command, *args)
            elif fetchval:
                result = await connection.fetchval(command, *args)
            elif fetchrow:
                result = await connection.fetchrow(command, *args)
            elif execute:
                result = await connection.execute(command, *args)
        return result


    @contextlib.asynccontextmanager
    async def _transaction(self) -> AsyncIterator[asyncpg.Connection]:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASS,
                host=config.DB_HOST,
                database=config.DB_NAME,
            )
        async with self._pool.acquire() as conn:  # type: asyncpg.Connection
            async with conn.transaction():
                yield conn

    async def close(self) -> None:
        if self._pool is None:
            return None

        await self._pool.close()