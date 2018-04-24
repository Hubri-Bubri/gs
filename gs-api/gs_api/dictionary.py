from sqlbuilder.smartsql import Q, T
from .api import Database, DictCursor


database = Database(
    expression_type=Database.SqlbuilderCursor,
    cursor_type=DictCursor
)


class User:
    
    @classmethod
    async def select_by_login_password(cls, login, password):
        async with database.cursor() as cursor:
            return await cursor.fetchone(Q()
                .tables(T.users)
                .fields(T.users.user_name)
                .where((T.users.user_name == login) & (T.users.password == password)))

    @classmethod
    async def select_by_identity(cls, identity):
        async with database.cursor() as cursor:
            return await cursor.fetchone(Q()
                .tables((T.users & T.access).on(T.users.id == T.access.user))
                .fields(T.users.user_name, T.access.permissions)
                .where((T.users.user_name == identity)))
