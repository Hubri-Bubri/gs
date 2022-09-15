from asyncio import get_event_loop
from aiomysql import create_pool, SSCursor, DictCursor
from collections import defaultdict, OrderedDict
from collections.abc import Sequence
from sqlbuilder.smartsql import Q, T, Result
from sqlbuilder.smartsql.dialects import mysql
import logging


logger = logging.getLogger(__name__)


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
                        _cursor = cursor

                        def __init__(_self, tables=None, result=None):
                            super().__init__(tables=tables, result=result or Result(compile=self._compile))

                    yield _Query


class Query(Q):

    def __init__(self, tables=None, result=None):
        super().__init__(tables=tables, result=result)

    async def selectone(self):
        await self._cursor.execute(*super().select())
        return await self._cursor.fetchone()

    async def selectall(self):
        await self._cursor.execute(*super().select())
        return await self._cursor.fetchall()

    async def select(self):
        return await self.selectall()

    async def delete(self, *args, **kwargs):
        return await self._cursor.execute(*super().delete(*args, **kwargs))

    async def insert(self, *args, **kwargs):
        return await self._cursor.execute(*super().insert(*args, **kwargs))

    async def update(self, *args, **kwargs):
        await self._cursor.execute(*super().update(*args, **kwargs))
        
    @property
    def _cursor(self):
        raise NotImplementedError
