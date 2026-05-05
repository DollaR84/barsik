from setuptools import setup, find_packages


extras = {
    "bot": [
        "aiogram>=3.0.0",
        "aiogram-dialog>=2.1.0",
        "redis",
        "aiofiles",
    ],
    "db": [
        "alembic",
        "psycopg2-binary",
        "asyncpg",
        "sqlalchemy",
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
    ],
    "llm": [
        "openai",
    ],
}

extras["all"] = sorted({dep for deps in extras.values() for dep in deps})


setup(
    name='barsik',
    author='Ruslan Dolovaniuk',
    author_email='ruslan.dolovaniuk84@gmail.com',
    packages=find_packages(),
    package_data={"barsik": ["py.typed"]},
    zip_safe=False,
    description="Adapters set for basic software architecture development kit",
    use_scm_version={
        "version_scheme": "post-release",
        "local_scheme": "no-local-version",
    },
    setup_requires=["setuptools-scm"],
    python_requires=">=3.12",
    install_requires=[
        "dishka",
        "adaptix",
        "dature",
        "pydantic",
        "pydantic-settings",
    ],
    extras_require=extras,
)
