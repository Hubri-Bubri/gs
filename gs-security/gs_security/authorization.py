from aiohttp_security.abc import AbstractAuthorizationPolicy
from gs_api.dictionary import User, PermissionSchema


class DatabaseAuthorizationPolicy(AbstractAuthorizationPolicy):

    async def authorized_userid(self, identity):
        return True

    async def permits(self, identity, permission, context):
        user_permission_schema = await PermissionSchema.select_by_login(identity)
        target, domen = context.split(':')


        return permission in self.parse_permission_schema(user_permission_schema, target)

    def parse_permission_schema(self, user_permission_schema, target):
        for user, target, tag in map(lambda _: _.values(), user_permission_schema):
            if target in target:
                return [int(_.strip()) for _ in tag.split(',')]

        return []


async def check_credentials(username, password):
    return True if await User.select_by_login_password(username, password) else False
