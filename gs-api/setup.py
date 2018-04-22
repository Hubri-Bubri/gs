from setuptools import setup


prod_requires = [
    'sqlbuilder',
    'aiomysql'
]

setup(
    name='gs_api',
    install_requires=prod_requires,
    packages=['gs_api']
)
