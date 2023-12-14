from django.conf import settings
from django.db import ConnectionHandler
from django.utils.connection import ConnectionProxy

connections = ConnectionHandler()
connection = ConnectionProxy(connections, settings.TEST_DB_ALIAS)


def reset_queries():
    for conn in connections.all(initialized_only=True):
        conn.queries_log.clear()
