from pymilvus import connections

from app.core.config import settings

_ALIAS = "default"
_connected = False


def connect() -> None:
    global _connected
    if _connected:
        return
    connections.connect(
        alias=_ALIAS,
        host=settings.milvus_host,
        port=str(settings.milvus_port),
        db_name=settings.milvus_database,
    )
    _connected = True
