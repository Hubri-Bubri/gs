from setuptools import setup
from distutils.cmd import Command
from subprocess import Popen
import subprocess
from gs import __version__
from setuptools.command.test import test as TestCommand
import sys


class Npm(Command):
    user_options = [('static', None, None)]

    def run(self):
        self._run('npm', 'install')
        self._run('npm', 'run', 'build')

    def _run(self, *args):
        return subprocess.run(args=args, cwd=r'./assets')

    def initialize_options(self): ...

    def finalize_options(self): ...


prod_requires = [
    'aiohttp',
    'aiomysql',
    'aiohttp_jinja2'
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
