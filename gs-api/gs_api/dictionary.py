from sqlbuilder.smartsql import Q, T
from .api import Database, DictCursor


database = Database(
    host='localhost',
    port=3306,
    name='contactcenter',
    user='root',
    password='8888',
    expression_type=Database.SqlbuilderCursor,
    cursor_type=DictCursor
)


class User:
    async def select(self):
        async with database.cursor() as cursor:
            return await cursor.fetchall(Q()
                .tables(T.actions)
                .fields(T.actions.name)
                .fields(T.actions.id))
