import time
from enum import Enum
from aiohttp import hdrs, web
import asyncio

from aiohttp_jinja2 import template
from aiohttp_session import get_session
from uuid import uuid4
from aiohttp_security import remember, has_permission, login_required
from gs_security.authorization import check_credentials
from gs_security.permission import Permission
from gs_api.dictionary import Application, Company

from .environment import APPLICATION_DIR


routes = web.RouteTableDef()


@routes.get('/')
@template('index.html')
async def dashboard(request):
    return {'nocache': hash(uuid4())}


@routes.post('/session')
async def session(request):
    
    session = await get_session(request)
    form = await request.json()
    session['COMPANY_ID'] = form.get('company-id')

    return web.StreamResponse()


@routes.get('/application')
async def application(request):
    return web.json_response(await Application.select_by_company(request.query.get('company-id')))


@routes.get('/company')
async def company(request):
    session = await get_session(request)
    login = session.get('AIOHTTP_SECURITY')
    return web.json_response(await Company.select_by_login(login))


@routes.post('/authenticate')
async def authenticate(request):
    form = await request.json()

    login = form.get('login')
    password = form.get('password')

    response = web.HTTPOk()


    if await check_credentials(login, password):
        await remember(request, response, login)

        return response

    return web.HTTPUnauthorized()


# register static routes
routes.static('/static', f"{APPLICATION_DIR}/static")
