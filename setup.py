from setuptools import setup, find_packages

setup(
    name='barsik',
    version='1.2.0',
    author='Ruslan Dolovaniuk',
    author_email='ruslan.dolovaniuk84@gmail.com',
    packages=find_packages(),
    package_data={"barsik": ["py.typed"]},
    zip_safe=False,
    description="Adapters set for basic software architecture development kit",
    python_requires=">=3.12",
    install_requires=[
        "dishka",
        "adaptix",
        "dature",
        "pydantic",
        "pydantic-settings",
    ],
    extras_require={
        "bot": [
            "aiogram",
            "aiogram-dialog",
            "redis",
            "aiofiles",
        ],
        "db": [
            "sqlalchemy"
        ],
        "redis": [
            "redis",
        ],
        "localisation": [
            "aiofiles",
        ],
        "geo": [
            "geopy",
            "shapely",
            "pyproj",
        ],
        "http": [
            "aiohttp",
            "requests",
            "descanso",
        ]
    }
)
