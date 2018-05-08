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
                .tables(T.user)
                .fields(T.user.login)
                .where((T.user.login == login) & (T.user.password == password)))


class PermissionSchema:
    @classmethod
    async def select_by_login(cls, login):
        async with database.cursor() as cursor:
            return await cursor.fetchall(Q()
                .tables((T.user & T.user_permission_schema).on(T.user.id == T.user_permission_schema.user_id))
                .fields(T.user.user_name, T.user_permission_schema.target, T.user_permission_schema.permission)
                .where(T.user.user_name == login))


class Application:
    @classmethod
    async def select_by_login(cls, login):
        async with database.cursor() as cursor:
            return await cursor.fetchall(Q()
                .tables((T.application & T.user & T.m2m_company_application).on(
                    (T.application.id == T.m2m_company_application.application_id) &
                    (T.users.id == T.m2m_company_application.user_id)
                ))
                .fields(T.application.name, T.application.link)
                .where(T.users.user_name == login))


class Company:
    @classmethod
    async def select_by_login(cls, login):
        async with database.cursor() as cursor:
            return await cursor.fetchall(Q()
                .tables((T.company & T.user & T.m2m_user_company).on(
                    (T.company.id == T.m2m_user_company.company_id) &
                    (T.user.id == T.m2m_user_company.user_id)
                ))
                .fields(T.company.id, T.company.name)
                .where(T.user.login == login))
