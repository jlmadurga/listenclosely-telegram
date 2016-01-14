from django.conf import settings


LISTENCLOSELY_TELEGRAM_BOT_TOKEN = getattr(settings, 'LISTENCLOSELY_TELEGRAM_BOT_TOKEN', None)