from django.contrib import admin
from .models import (People,ReceptionistDisplayMessage,
                     Profile,Message,Meeting,Voice)

# Register your models here.

admin.site.register(People)
admin.site.register(ReceptionistDisplayMessage)
admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Meeting)
admin.site.register(Voice)
