# coding=utf-8
from factory import Sequence, SubFactory, Factory
from twx.botapi import Update, Message, User, Chat
from datetime import datetime
from factory.fuzzy import FuzzyText

class UserFactory(Factory):
    class Meta:
        model = User
    id = Sequence(lambda n: 'user_id_%d' % n)
    first_name = Sequence(lambda n: 'first_name_%d' % n)
    last_name = Sequence(lambda n: 'last_name_%d' % n)
    username = Sequence(lambda n: 'username_%d' % n)

class ChatFactory(Factory):
    class Meta:
        model = Chat
    id = Sequence(lambda n: 'chat_id_%d' % n)
    type = "private"
    title = Sequence(lambda n: 'title_%d' % n)
    username = Sequence(lambda n: 'username_%d' % n)
    first_name = Sequence(lambda n: 'first_name_%d' % n)
    last_name = Sequence(lambda n: 'last_name_%d' % n)

class MessageFactory(Factory):
    class Meta:
        model = Message
    message_id = Sequence(lambda n: 'message_id_%d' % n)
    sender = SubFactory(UserFactory)
    date = datetime.now()
    chat = SubFactory(ChatFactory)
    forward_from = None
    forward_date = None
    reply_to_message = None
    text = FuzzyText()
    audio = None
    document = None
    photo = None
    sticker = None
    video = None
    voice = None
    caption = None
    contact = None
    location = None
    new_chat_participant = None
    left_chat_participant = None
    new_chat_title = None
    new_chat_photo = None
    delete_chat_photo = None
    group_chat_created = None
    

class UpdateFactory(Factory):
    class Meta:
        model = Update
    update_id = Sequence(lambda n: n)
    message = SubFactory(MessageFactory)