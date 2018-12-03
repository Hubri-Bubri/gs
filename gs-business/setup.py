from setuptools import setup
from distutils.cmd import Command
from subprocess import Popen
import subprocess
from gs_business import __version__


class Npm(Command):
    user_options = [('static', None, None)]

    def run(self):
        self._run('npm', 'install')
        self._run('npm', 'run', 'build')

    def _run(self, *args):
        return subprocess.run(args=args, cwd=r'./assets')

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


prod_requires = [
    'aiohttp',
    'aiohttp_jinja2',
    'aiohttp_security',
    'aiohttp_session',
    'gs_api',
    'gs_security',
    'gs_configurator'
]

setup(
    name='gs-business',
    version=__version__,
    install_requires=prod_requires,
    packages=['gs_business'],
    package_data={
        'gs_business': [
            'static/*',
            'static/bundle/*',
            'static/bundle/font-awesome/css/*',
            'static/bundle/font-awesome/webfonts/*'
        ]
    },
    include_package_data=True,
    cmdclass={'static': Npm}
)
