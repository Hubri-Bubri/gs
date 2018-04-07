from aiohttp.web import Application, run_app
import aiohttp_jinja2
from jinja2 import FileSystemLoader

from .action import routes
from .environment import APPLICATION_DIR


__version__ = '0.0.1'


def run():
    application = Application()

    application.router.add_routes(routes)
    aiohttp_jinja2.setup(application, loader=FileSystemLoader(f"{APPLICATION_DIR}/static"))

    return run_app(application, host='0.0.0.0', port=8080)
