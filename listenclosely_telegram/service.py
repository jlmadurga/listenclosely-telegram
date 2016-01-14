# -*- coding: utf-8 -*-
from listenclosely.services.base import BaseMessageServiceBackend
from listenclosely_telegram import conf 
import logging
from listenclosely_telegram.bot import Bot

logger = logging.getLogger(__name__)

class TelegramMessageServiceBackend(BaseMessageServiceBackend):
    """
    Message Service Backend implementation to send instant messages with telepot
    """
    
    def __init__(self, caller, fail_silently=False, **kwargs):
        super(TelegramMessageServiceBackend, self).__init__(fail_silently, **kwargs)
        try:
            self.listening = False
            self.bot = Bot(conf.LISTENCLOSELY_TELEGRAM_BOT_TOKEN)
        except:
            logger.error("Configuration Error")
            raise
        self.caller = caller
        
    def listen(self):
        """
        Loop to receive messages from whatsapp server. Set autoconnect option to True
        """
        if not self.bot.listening:
            self.bot.listen(self.on_message)   
        else:
            logger.warning("Already listening")
            
    def send_message(self, id_service, content):
        """
        Send message to a 
        """
        message = self.bot.send_message(id_service, content).wait()
        return message.message_id      

    def disconnect(self):
        """
        Disconnect from connection
        """
        self.bot.listening = False
        logger.warning("Disconnect")
        
    def on_message(self, message):
        self.caller.on_message(message.message_id, message.sender.id, message.text)