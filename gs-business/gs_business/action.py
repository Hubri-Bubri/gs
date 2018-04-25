from aiohttp import hdrs, web
from aiohttp_jinja2 import template
from aiohttp_session import get_session
from uuid import uuid4
import time
from aiohttp_security import remember, has_permission, login_required
from gs_security.authorization import check_credentials
from gs_api.dictionary import Application 

from .environment import APPLICATION_DIR


routes = web.RouteTableDef()


@routes.get('/')
@template('index.html')
@has_permission('first')
async def dashboard(request):
    return {'nocache': hash(uuid4())}


@routes.get('/application')
@has_permission('first')
async def security(request):
    session = await get_session(request)
    identity = session.get('AIOHTTP_SECURITY')

    return web.json_response(await Application.select_by_login(identity))



# register static routes
routes.static('/static', f"{APPLICATION_DIR}/static")
