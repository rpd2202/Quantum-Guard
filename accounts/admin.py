from django.contrib import admin
from .models import secret_keys,Message

# Register your models here.

admin.site.register(secret_keys)
admin.site.register(Message)
