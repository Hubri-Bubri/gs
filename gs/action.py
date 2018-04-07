from aiohttp import hdrs, web
from aiohttp_jinja2 import template
from uuid import uuid4

from .environment import APPLICATION_DIR


routes = web.RouteTableDef()


@routes.get('/')
@template('index.html')
async def dashboard(request):
    return {'nocache': hash(uuid4())}


@routes.get('/upload')
async def upload(request):
    return web.Response(text='OK')

# register static routes
routes.static('/static', f"{APPLICATION_DIR}/static")
