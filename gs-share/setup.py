from setuptools import setup


setup(
    name='gs_share',
    packages=['gs_share'],
    include_package_data=True,
    package_data={
        'gs_share': [
            'resources/*',
        ]
    },
    version="0.1.1"
)
