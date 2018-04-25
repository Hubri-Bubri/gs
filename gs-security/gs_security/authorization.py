from aiohttp_security.abc import AbstractAuthorizationPolicy
from gs_api.dictionary import User


class DatabaseAuthorizationPolicy(AbstractAuthorizationPolicy):

    async def authorized_userid(self, identity):
        return True

    async def permits(self, identity, permission, context=None):
        user = await User.select_by_identity(identity)

        if user is None:
            return False

        return permission in self.parse_permission_dsl(user.get('permissions', None))

    def parse_permission_dsl(self, permission):
        if permission is None:
            return []

        return [_.strip() for _ in permission.split(',')]


async def check_credentials(username, password):
    return True if await User.select_by_login_password(username, password) else False
