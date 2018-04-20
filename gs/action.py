from aiohttp import hdrs, web
from aiohttp_jinja2 import template
from uuid import uuid4

from .environment import APPLICATION_DIR
from .service import User

routes = web.RouteTableDef()

# api
user_service = User()


@routes.get('/')
@template('index.html')
async def dashboard(request):
    return {'nocache': hash(uuid4())}

@routes.get('/user/{name}')
async def user(request):

    return web.Response(text=await user_service.select(request.match_info['name']))


@routes.post('/authorization')
async def  api_bgp_show_route(request):
      data = await request.json()
      return web.Response(text=await user_service.select(data['name'], data['password'],  data['companyid']))



# register static routes
routes.static('/static', f"{APPLICATION_DIR}/static")
