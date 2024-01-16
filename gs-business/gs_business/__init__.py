import aiohttp_session
import aiohttp_security
import aiohttp_jinja2
import argparse
parser = argparse.ArgumentParser(description="Example of a single flag acting as a boolean and an option.")
parser.add_argument('--apparthotel', nargs='?', const="1", default=False)
parser.add_argument('--demo', nargs='?', const="1", default=False)
parser.add_argument('--bwsa', nargs='?', const="1", default=False)
parser.add_argument('--awe', nargs='?', const="1", default=False)
parser.add_argument('--awerus', nargs='?', const="1", default=False)
parser.add_argument('--bundw', nargs='?', const="1", default=False)
parser.add_argument('--christ', nargs='?', const="1", default=False)
parser.add_argument('--baer', nargs='?', const="1", default=False)
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




def run(max_size=0):
    application = Application(client_max_size=10024 ** 2)
    application.router.add_routes(routes)
    aiohttp_jinja2.setup(application, loader=FileSystemLoader(f"{APPLICATION_DIR}/static"))
    aiohttp_session.setup(application, SimpleCookieStorage(domain='awe.do'))
    # aiohttp_session.setup(application, SimpleCookieStorage())
    aiohttp_security.setup(application, SessionIdentityPolicy(), DatabaseAuthorizationPolicy())

    # aiohttp_dashboard.setup('dashboard', application)

    # do load file configuraion
    configuration.load()
    # do load database configuraion

    if args.baer:
        listen=8090
        dictionary.database.set_configuration(
            host=configuration['database']['host'],
            port=configuration['database']['port'],
            name='baer',
            user=configuration['database']['user'],
            password=configuration['database']['password']
        )
    if args.apparthotel:
        listen=8089
        dictionary.database.set_configuration(
            host=configuration['database']['host'],
            port=configuration['database']['port'],
            name='apparthotel',
            user=configuration['database']['user'],
            password=configuration['database']['password']
        )
    if args.demo:
        listen=8079
        dictionary.database.set_configuration(
            host=configuration['database']['host'],
            port=configuration['database']['port'],
            name='demo',
            user=configuration['database']['user'],
            password=configuration['database']['password']
        )
    if args.bwsa:
        listen=8081
        dictionary.database.set_configuration(
            host=configuration['database']['host'],
            port=configuration['database']['port'],
            name='bwsa',
            user=configuration['database']['user'],
            password=configuration['database']['password']
        )
    if args.awe:
        listen=8082
        dictionary.database.set_configuration(
            host=configuration['database']['host'],
            port=configuration['database']['port'],
            name='awe_gmbh',
            user=configuration['database']['user'],
            password=configuration['database']['password']
        )
    if args.bundw:
        listen=8083
        dictionary.database.set_configuration(
            host=configuration['database']['host'],
            port=configuration['database']['port'],
            name='bundw',
            user=configuration['database']['user'],
            password=configuration['database']['password']
        )
    if args.christ:
        listen=8084
        dictionary.database.set_configuration(
            host=configuration['database']['host'],
            port=configuration['database']['port'],
            name='christ',
            user=configuration['database']['user'],
            password=configuration['database']['password']
        )
    return run_app(application, host='127.0.0.1', port=listen)
