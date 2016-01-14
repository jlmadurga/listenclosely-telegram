from twx.botapi import TelegramBot

class Bot(TelegramBot):
    
    def __init__(self, token):
        TelegramBot.__init__(self, token)
        self.listening = False
        self.offset = None
        #  TODO: parametrize in settings
        self.timeout = 1
        
    def listen(self, on_message):
        self.listening = True
        while self.listening:
            updates = self.get_updates(offset=self.offset, timeout=self.timeout).wait()
            for update in updates:
                self.offset = max(self.offset, update.update_id+1)
                #  TODO: only manage text messages
                if update.message.text:
                    on_message(update.message)