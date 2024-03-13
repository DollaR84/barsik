from setuptools import setup, find_packages

setup(
    name='barsik',
    version='0.7.3',
    author='Ruslan Dolovaniuk',
    author_email='ruslan.dolovaniuk84@gmail.com',
    packages=find_packages(),
    package_data={"barsik": []},
    description='Adapters set for basic software architecture development kit',
    install_requires=[
        "pydantic",
        "dishka"
    ],
    extras_require={
        "bot": [
            "aiogram",
            "aiogram-dialog",
            "aioredis",
            "aiofiles",
        ],
        "db": [
            "sqlalchemy"
        ],
        "redis": [
            "aioredis",
        ],
        "localisation": [
            "aiofiles",
        ],
        "geo": [
            "geopy",
            "shapely",
            "pyproj",
        ]
    }
)
