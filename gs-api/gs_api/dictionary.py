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
 
    @classmethod
    async def select_by_login(cls, login):
        async with database.cursor() as cursor:
            return await cursor.fetchone(Q()
                .tables(T.user)
                .fields(T.user.login, T.user.first_name, T.user.second_name)
                .where((T.user.login == login)))

    @classmethod
    async def select_roles_by_login(cls, login):
        async with database.cursor() as cursor:
            return await cursor.fetchall(Q()
                .tables((T.role & T.m2m_user_role & T.user).on(
                        (T.role.id == T.m2m_user_role.role_id) &
                        (T.user.id == T.m2m_user_role.user_id)))
                .fields(T.role.name)
                .where((T.user.login == login)))

    @classmethod
    async def select_profile(cls, login, company_id):
        async with database.cursor() as cursor:
            return {
                'account': await cls.select_by_login(login),
                'roles': await cls.select_roles_by_login(login),
                'selected-company': await Company.select_by_id(company_id),
                'access-user': await PermissionSchema.select_by_login(login),
                'access-role': await PermissionSchema.select_by_login(login)
            }

class PermissionSchema:
    @classmethod
    async def select_by_login(cls, login):
        async with database.cursor() as cursor:
            return await cursor.fetchall(Q()
                .tables((T.user & T.user_permission_schema).on(T.user.id == T.user_permission_schema.user_id))
                .fields(T.user.login,
                        T.user_permission_schema.target,
                        T.user_permission_schema.permission,
                        T.user_permission_schema.domen)
                .where(T.user.login == login))


class Application:
    @classmethod
    async def select_by_company(cls, company_id):
        async with database.cursor() as cursor:
            return await cursor.fetchall(Q()
                .tables((T.application & T.m2m_company_application).on(
                         T.application.id == T.m2m_company_application.application_id))
                .fields(T.application.name, T.application.link)
                .where(T.m2m_company_application.company_id == company_id))


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

    @classmethod
    async def select_by_id(cls, id):
        async with database.cursor() as cursor:
            return await cursor.fetchone(Q()
                .tables(T.company)
                .fields(T.company.name)
                .where(T.company.id == id))

class Project:
    @classmethod
    async def select_project(cls, id):
        async with database.cursor() as cursor:
            return await cursor.fetchone(Q()
                .tables(T.project & T.user).on(T.project.user_id == T.user.id)
                .fields(T.project.project_number, T.project.date, T.project.street,
                    T.project.city, T.project.zip, T.user.first_name, T.user.second_name)
                .where(T.project.id == id))

class Projects:
    @classmethod
    async def select_projects(cls):
        async with database.cursor() as cursor:
            return await cursor.fetchall(Q()
                .tables(T.project)
                .fields(T.project.project_number, T.project.date, T.project.street,
                    T.project.city, T.project.zip, T.project.status_set, T.project.id, T.project.other
                    ))
class Offer:
    @classmethod
    async def select_offer(cls, id):
        async with database.cursor() as cursor:
            return await cursor.fetchall(Q()
                .tables(T.offer)
                .fields(T.offer.offer_number, T.offer.status_set, T.offer.other)
                .where(T.offer.project_id == id))
class Invoice:
    @classmethod
    async def select_invoice(cls, id):
        async with database.cursor() as cursor:
            return await cursor.fetchall(Q()
                .tables(T.invoice)
                .fields(T.invoice.invoice_number, T.invoice.status_set, T.invoice.other)
                .where(T.invoice.project_id == id))

class Add_offer:
    @classmethod
    async def add_offer(cls):
            async with database.cursor() as cursor:
                return await cursor._cursor.execute("INSERT INTO offer (other) VALUES(%s)", [1])

#return await cursor.Q(T.offer).insert()
# print (add_work)
# print (add_insurance_number)
# print (add_place)
# print (add_comment)