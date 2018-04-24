from aiohttp import hdrs, web
from aiohttp_jinja2 import template
from aiohttp_session import get_session
from uuid import uuid4
import time
from aiohttp_security import remember, has_permission, login_required

from .environment import APPLICATION_DIR
from gs_security.authorization import check_credentials


routes = web.RouteTableDef()

@routes.get('/')
@template('index.html')
async def dashboard(request):
    return {'nocache': hash(uuid4())}

@routes.get('/security')
@has_permission('bla')
async def security(request):
    session = await get_session(request)

    return web.Response(text='Yes')


@routes.get('/login')
async def login(request):
    
    login = request.query.get('login')
    password = request.query.get('password')
    response = web.Response(text='Hello')

    if await check_credentials(login, password):

        await remember(request, response, login)
        return response


    return web.HTTPUnauthorized(text='Invalid username/password combination')


# register static routes
routes.static('/static', f"{APPLICATION_DIR}/static")
