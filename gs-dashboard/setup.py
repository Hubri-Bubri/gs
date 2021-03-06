from setuptools import setup
from distutils.cmd import Command
from subprocess import Popen
import subprocess
from gs_dashboard import __version__


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
    'aiomysql',
    'aiohttp_jinja2',
    'aiohttp_security'
]

setup(
    name='gs',
    version=__version__,
    install_requires=prod_requires,
    packages=['gs'],
    package_data={
        'gs': [
            'static/*',
            'static/bundle/*',
            'static/bundle/font-awesome/css/*',
            'static/bundle/font-awesome/webfonts/*'
        ]
    },
    include_package_data=True,
    cmdclass={'static': Npm}
)
