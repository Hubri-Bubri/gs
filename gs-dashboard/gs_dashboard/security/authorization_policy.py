from aiohttp_security.abc import AbstractAuthorizationPolicy
from gs_api.dictionary import User


user_service = User()


class DatabaseAuthorizationPolicy(AbstractAuthorizationPolicy):
    
    async def authorized_userid(self, identity):
        return True

    async def permits(self, identity, permission, context=None):
        user = await user_service.select_by_identity(identity)

        if user is None:
            return False

        return permission in self.parse_permission_dsl(user.get('permissions', None))

    def parse_permission_dsl(self, permission):
        if permission is None:
            return []

        return permission.split(',')


async def check_credentials(username, password):
    return True if await user_service.select_by_login_password(username, password) else False

