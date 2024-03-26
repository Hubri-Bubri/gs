from setuptools import setup


prod_requires = [
    'sqlbuilder',
    'aiomysql',
    'gs_share'
]
setup(
    name='gs_api',
    install_requires=prod_requires,
    packages=['gs_api'],
    version="0.1.23"
)
