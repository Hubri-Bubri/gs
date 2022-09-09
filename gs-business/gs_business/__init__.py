import aiohttp_session
import aiohttp_security
import aiohttp_jinja2
import argparse
parser = argparse.ArgumentParser(description="Example of a single flag acting as a boolean and an option.")
parser.add_argument('--bwsa', nargs='?', const="1", default=False)
parser.add_argument('--ah', nargs='?', const="1", default=False)
parser.add_argument('--awe', nargs='?', const="1", default=False)
parser.add_argument('--test', nargs='?', const="1", default=False)
parser.add_argument('--christhs', nargs='?', const="1", default=False)
args = parser.parse_args()

# import aiohttp_dashboard


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
    aiohttp_session.setup(application, SimpleCookieStorage(domain='awe.do'))
    # aiohttp_session.setup(application, SimpleCookieStorage())
    aiohttp_security.setup(application, SessionIdentityPolicy(), DatabaseAuthorizationPolicy())

    # aiohttp_dashboard.setup('dashboard', application)

    # do load file configuraion
    configuration.load()
    # do load database configuraion
   
    if args.bwsa:
        listen=8081
        dictionary.database.set_configuration(
            host=configuration['database']['host'],
            port=configuration['database']['port'],
            name='bwsa',
            user=configuration['database']['user'],
            password=configuration['database']['password']
        )
    if args.ah:
        listen=8082
        dictionary.database.set_configuration(
            host=configuration['database']['host'],
            port=configuration['database']['port'],
            name='ah',
            user=configuration['database']['user'],
            password=configuration['database']['password']
        )
    if args.awe:
        listen=8083
        dictionary.database.set_configuration(
            host=configuration['database']['host'],
            port=configuration['database']['port'],
            name='awe_gmgh',
            user=configuration['database']['user'],
            password=configuration['database']['password']
        )
    if args.test:
        listen=8084
        dictionary.database.set_configuration(
            host=configuration['database']['host'],
            port=configuration['database']['port'],
            name='test',
            user=configuration['database']['user'],
            password=configuration['database']['password']
        )
    if args.christhs:
        listen=8085
        dictionary.database.set_configuration(
            host=configuration['database']['host'],
            port=configuration['database']['port'],
            name='ChristHS',
            user=configuration['database']['user'],
            password=configuration['database']['password']
        )
    return run_app(application, host='127.0.0.1', port=listen)