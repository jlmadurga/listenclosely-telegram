#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from tests.factories import UpdateFactory
import threading
from django.conf import settings
settings.configure(
    DEBUG=True,
    USE_TZ=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
        }
    },
    ROOT_URLCONF="listenclosely.urls",
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sites",
        "listenclosely_telegram",
    ],
    SITE_ID=1,
    MIDDLEWARE_CLASSES=(),
    LISTENCLOSELY_TELEGRAM_BOT_TOKEN="token",
)

try:
    import django
    setup = django.setup
except AttributeError:
    pass
else:
    setup()

try:
    from unittest import mock
except ImportError:
    import mock  # noqa

class TestService(unittest.TestCase):
    
    def setUp(self):
        self.caller = mock.MagicMock()
        from listenclosely_telegram.service import TelegramMessageServiceBackend
        self.service = TelegramMessageServiceBackend(self.caller)
        
    def _queue_thread(self, fn, *args, **kwargs):
        while not self.service.bot.listening:
            pass
        if fn:
            fn(*args, **kwargs)
        
    def _listen(self, asyn_action, timeout=0.3):
        self.input_thread = threading.Thread(target=self._queue_thread, args=(asyn_action,))
        self.input_thread.daemon = True
        self.input_thread.start()
        self.service.listen()
        self.assertFalse(self.service.bot.listening)
        
    def _disconnect(self):
        self.assertTrue(self.service.bot.listening)
        self.service.disconnect()
        
    def test_caller_assigned(self):       
        self.assertEqual(self.service.caller, self.caller)
        
    def test_disconnect(self):
        self.updates = [UpdateFactory()]
        with mock.patch('twx.botapi.TelegramBot.get_updates', callable=mock.MagicMock()) as mock_get_updates:
            mock_get_updates.return_value.wait = mock.MagicMock(return_value=self.updates)
            self._listen(self._disconnect)
            
    def test_offset(self):
        self.updates = [UpdateFactory()]
        with mock.patch('twx.botapi.TelegramBot.get_updates', callable=mock.MagicMock()) as mock_get_updates:
            mock_get_updates.return_value.wait = mock.MagicMock(return_value=self.updates)
            self._listen(self._disconnect)
            self.assertEqual(self.service.bot.offset-1, self.updates[0].update_id)
         
if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
