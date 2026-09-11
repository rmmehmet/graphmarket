from neo4j import Driver, GraphDatabase

from app.core.config import settings

_driver: Driver | None = None


def get_driver() -> Driver:
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password)
        )
    return _driver


def get_session():
    return get_driver().session(database=settings.neo4j_database)
