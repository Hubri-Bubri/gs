from aiohttp_security.abc import AbstractAuthorizationPolicy


user_map = {
    'alex': {
        'permission': ['read', 'write']
    }
}


class DatabaseAuthorizationPolicy(AbstractAuthorizationPolicy):
    
    async def authorized_userid(self, identity):
        
        if identity in user_map.keys():
            return identity

    async def permits(self, identity, permission, context=None):
        user = user_map.get(identity, None)
        
        if user is None:
            return False

        return permission in user.get('permission')


async def check_credentials(user_map, username, password):
    user = user_map.get(username)
    if not user:
        return False

    return user.password == password
