from asyncio import get_event_loop
from aiomysql import create_pool, SSCursor, DictCursor
from collections import defaultdict, OrderedDict, Sequence
from sqlbuilder.smartsql import Q, T
from sqlbuilder.smartsql.dialects.mysql import compile as mysql_compile
import logging


logger = logging.getLogger(__name__)


from gs_share import aiocontextmanager


class Database:
    _host = None
    _port = None
    _name = None
    _user = None
    _password = None

    _expression_type = None
    _cursor_type = None

    def __init__(self, *, host=None, port=None, name=None, user=None, password=None, expression_type=None, cursor_type=None):
        self._host = host
        self._port = port
        self._name = name
        self._user = user
        self._password = password

        self._expression_type = self.SqlbuilderCursor
        self._cursor_type = DictCursor

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
            raise NotImplementedError

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
