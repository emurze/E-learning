import os
import socket

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class MyLiveServerTestCase(StaticLiveServerTestCase):
    host = os.getenv(
        'STAGING_SERVER', socket.gethostbyname(socket.gethostname())
    )
    print('\n' * 6, host, '\n' * 6)
    port = 8081
