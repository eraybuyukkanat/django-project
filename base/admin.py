from django.contrib import admin

from .models import Room, Topic, Message

admin.site.register(Room) #Admin paneline kaydettik
admin.site.register(Topic)
admin.site.register(Message)