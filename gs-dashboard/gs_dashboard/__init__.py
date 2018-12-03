import aiohttp_session
import aiohttp_security
import aiohttp_jinja2
from aiohttp_session import SimpleCookieStorage
from aiohttp_security import SessionIdentityPolicy
from aiohttp.web import Application, run_app
from jinja2 import FileSystemLoader

from gs_api import dictionary
from gs_security import DatabaseAuthorizationPolicy

from .action import routes
from .environment import APPLICATION_DIR, configuration


__version__ = '0.0.1'


def run():
    application = Application()
    
    application.router.add_routes(routes)
    
    aiohttp_jinja2.setup(application, loader=FileSystemLoader(f"{APPLICATION_DIR}/static"))
    aiohttp_session.setup(application, SimpleCookieStorage())
    aiohttp_security.setup(application, SessionIdentityPolicy(), DatabaseAuthorizationPolicy())

    # do load file configuraion
    configuration.load()
    # do load database configuraion
    dictionary.database.set_configuration(
        host=configuration['database']['host'],
        port=configuration['database']['port'],
        name=configuration['database']['name'],
        user=configuration['database']['user'],
        password=configuration['database']['password']
    )

    return run_app(application, host='0.0.0.0', port=configuration['application']['dashboard']['listen'])
