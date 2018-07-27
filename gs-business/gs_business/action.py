import time
from aiohttp import web
from aiohttp_jinja2 import template
from aiohttp_session import get_session
from uuid import uuid4
from aiohttp_security import remember, has_permission, login_required
from gs_security.authorization import check_credentials
from gs_api.dictionary import Application, User, Project, Projects, Offer, Invoice, Add_offer

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

@routes.get('/projects')
async def method (request):
    return web.json_response(await Projects.select_projects())

@routes.get('/offer')
async def method (request):
    return web.json_response(await Offer.select_offer(request.query['id']))

@routes.get('/invoice')
async def method (request):
    return web.json_response(await Invoice.select_invoice(request.query['id']))

@routes.get('/add_offer')
async def method (request):
   # return web.json_response(await Add_offer.add_offer(request.query['add_work'], request.query['add_insurance_number'], request.query['add_place'], request.query['add_comment']))
    return web.json_response(await Add_offer.add_offer())

# register static routes
routes.static('/static', f"{APPLICATION_DIR}/static")
