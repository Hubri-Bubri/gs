from asyncio import get_event_loop
from aiomysql import create_pool, SSCursor, DictCursor
from collections import defaultdict, OrderedDict, Sequence
from sqlbuilder.smartsql import Q, T
from sqlbuilder.smartsql.dialects.mysql import compile as mysql_compile

from gs_share import aiocontextmanager


class Database:
    _host = None
    _port = None
    _name = None
    _user = None
    _password = None

    _expression_type = None
    _cursor_type = None

    def __init__(self, host, port, name, user, password, expression_type, cursor_type):
        self._host = host
        self._port = port
        self._name = name
        self._user = user
        self._password = password

        self._expression_type = expression_type
        self._cursor_type = cursor_type

    def pool(self):
        raise NotImplementedError()

    def connection(self):
        raise NotImplementedError()

    @aiocontextmanager
    async def cursor(self):
        async with create_pool(host=self._host, port=self._port, user=self._user,
                               password=self._password, db=self._name) as pool:

            async with pool.get() as connection:
                async with connection.cursor(self._cursor_type) as cursor:
                    yield self._expression_type(cursor)

    class Cursor:
        """ Shortcut facade for python db-api 2.0 cursor """

        def __init__(self, cursor):
            self._cursor = cursor

        async def execute(self):
            raise NotImplementedError()

        async def fetchall(self, *args, **kwargs):
            await self.execute(*args, **kwargs)
            return await self._cursor.fetchall()

        async def fetchone(self, *args, **kwargs):
            await self.execute(*args, **kwargs)
            return await self._cursor.fetchone()

    class SqlbuilderCursor(Cursor):
        """ sqlbuilder.smartsql aware api """
        
        async def execute(self, query):
            return await self._cursor.execute(*mysql_compile(query))
