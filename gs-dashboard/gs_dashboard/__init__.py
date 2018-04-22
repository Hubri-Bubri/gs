import aiohttp_debugger
import aiohttp_session
import aiohttp_security
import aiohttp_jinja2
from aiohttp_session import SimpleCookieStorage
from aiohttp_security import SessionIdentityPolicy
from aiohttp.web import Application, run_app
from jinja2 import FileSystemLoader

from .action import routes
from .environment import APPLICATION_DIR
from .security.authorization_policy import DatabaseAuthorizationPolicy


__version__ = '0.0.1'


def run():
    application = Application()
    
    application.router.add_routes(routes)
    
    aiohttp_jinja2.setup(application, loader=FileSystemLoader(f"{APPLICATION_DIR}/static"))
    aiohttp_session.setup(application, SimpleCookieStorage())
    aiohttp_security.setup(application, SessionIdentityPolicy(), DatabaseAuthorizationPolicy())

    return run_app(application, host='0.0.0.0', port=8080)
