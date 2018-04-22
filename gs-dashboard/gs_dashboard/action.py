from aiohttp import hdrs, web
from aiohttp_jinja2 import template
from aiohttp_session import get_session
from uuid import uuid4
import time
from aiohttp_security import (
    remember,
    forget,
    authorized_userid,
    has_permission,
    login_required
)

from .environment import APPLICATION_DIR
from .security.authorization_policy import check_credentials

routes = web.RouteTableDef()



@routes.get('/security')
async def security(request):
    session = await get_session(request)

    session['time'] = time.time()
    
    return web.Response(text='security')


@routes.get('/login')
async def login(request):

    # verified = await check_credentials(request.app.user_map, username, password)
    response = web.Response(text='login')
    await remember(request, response, 'username')
    return response


# register static routes
routes.static('/static', f"{APPLICATION_DIR}/static")
