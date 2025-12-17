from asyncio import Server
from django.contrib import admin

# Register your models here.
from .models import Location, Service, Subscription


admin.site.register([Location, Service, Subscription])