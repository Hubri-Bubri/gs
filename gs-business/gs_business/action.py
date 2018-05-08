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
async def dashboard(request):
    return {'nocache': hash(uuid4())}


# register static routes
routes.static('/static', f"{APPLICATION_DIR}/static")
