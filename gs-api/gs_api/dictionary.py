from sqlbuilder.smartsql import Q, T
from .api import Database, DictCursor


database = Database(
    expression_type=Database.SqlbuilderCursor,
    cursor_type=DictCursor
)


class User:
    async def select_by_login_password(self, login, password):
        async with database.cursor() as cursor:
            return await cursor.fetchone(Q()
                .tables(T.users)
                .fields(T.users.user_name)
                .where((T.users.user_name == login) & (T.users.password == password)))


    async def select_by_identity(self, identity):
        async with database.cursor() as cursor:
            return await cursor.fetchone(Q()
                .tables((T.users & T.access).on(T.users.id == T.access.user))
                .fields(T.users.user_name, T.access.permissions)
                .where((T.users.user_name == identity)))
