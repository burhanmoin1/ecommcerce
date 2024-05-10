from django_mongoengine import Document, fields
from datetime import datetime

class SuperUser(Document):
    username = fields.StringField(unique=True, blank=False)
    email = fields.EmailField(blank=False, unique=True)
    password = fields.StringField(blank=False)
    is_superuser = fields.BooleanField(default=False)
    token = fields.StringField(blank=True)
    login_time = fields.DateTimeField(blank=True)
    session_token = fields.StringField(blank=True)

class SuperUserSession(Document):
    superuser = fields.ReferenceField(SuperUser, blank=False)
    session_id = fields.StringField(unique=True) 
    created_at = fields.DateTimeField(default=datetime.now)
    last_activity = fields.DateTimeField(default=datetime.now)
    is_active = fields.BooleanField(default=True)
