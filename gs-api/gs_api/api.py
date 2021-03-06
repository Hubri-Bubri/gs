from asyncio import get_event_loop
from aiomysql import create_pool, SSCursor, DictCursor
from collections import defaultdict, OrderedDict, Sequence
from sqlbuilder.smartsql import Q, T, Result
from sqlbuilder.smartsql.dialects import mysql
from gs_share import aiocontextmanager


class Database:

    def __init__(self, *, host=None, port=None, name=None, user=None, password=None, cursor_type=None, compile=None):
        self._host = host
        self._port = port
        self._name = name
        self._user = user
        self._password = password
        self._cursor_type = DictCursor
        self._compile = compile

    def set_configuration(self, host, port, name, user, password):
        self._host = host
        self._port = port
        self._name = name
        self._user = user
        self._password = password

    @aiocontextmanager
    def pool(self):
        raise NotImplementedError

    @aiocontextmanager
    def connection(self):
        raise NotImplementedError

    @aiocontextmanager
    async def query(self):
        async with create_pool(host=self._host, port=self._port, user=self._user,
                               password=self._password, db=self._name, autocommit=True) as pool:

            async with pool.get() as connection:
                async with connection.cursor(self._cursor_type) as cursor:

                    class _Query(Query):
                        def __init__(_self, tables=None, result=None):
                            super().__init__(tables=tables, result=result or Result(compile=self._compile))

                        @property
                        def _cursor(self):
                            return cursor

                    yield _Query


class Query(Q):

    async def selectone(self):
        await self._cursor.execute(*super().select())
        return await self._cursor.fetchone()

    async def selectall(self):
        await self._cursor.execute(*super().select())
        return await self._cursor.fetchall()

    async def select(self):
        return await self.selectall()

    async def count(self):
        await self._cursor.execute(*super().count())
        return await self._cursor.fetchone()

    async def insert(self, *args, **kwargs):
        await self._cursor.execute(*super().insert(*args, **kwargs))
        return await self._cursor.fetchone()

    async def update(self):
        await self._cursor.execute(*super().update(*args, **kwargs))
        return await self._cursor.fetchone()

    async def delete(self):
        await self._cursor.execute(*super().delete(*args, **kwargs))
        return await self._cursor.fetchone()

    @property
    def _cursor(self):
        raise NotImplementedError
