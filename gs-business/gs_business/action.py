import time
from aiohttp import web
from aiohttp_jinja2 import template
from aiohttp_session import get_session
from uuid import uuid4
from aiohttp_security import remember, has_permission, login_required
from gs_security.authorization import check_credentials
from gs_api.dictionary import Application, User, Project

from .environment import APPLICATION_DIR


routes = web.RouteTableDef()


@routes.get('/')
@template('index.html')
async def dashboard(request):
    return {'nocache': hash(uuid4())}


@routes.get('/profile')
async def profile(request):
    session = await get_session(request)
    return web.json_response(await User.select_profile(session.get('AIOHTTP_SECURITY'), session.get('COMPANY_ID')))

@routes.get('/project_detail')
async def method (request):
    return web.json_response(await Project.select_project(request.query['id']))


# register static routes
routes.static('/static', f"{APPLICATION_DIR}/static")
