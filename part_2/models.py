from mongoengine import connect, Document, StringField, BooleanField

from part_1.conf.conn import uri


# Модуль конфігурації з'єднання
connect(host=uri, ssl=True)


# Модель контакту
class Contact(Document):
    name = StringField(required=True, max_length=50)
    email = StringField(required=True, max_length=50)
    email_sent = BooleanField(default=False)
    phone = StringField(required=True, max_length=50)
    sms_sent = BooleanField(default=False)
    meta = {"collection": "contacts"}
