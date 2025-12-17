from django.contrib import admin
from django.contrib.auth.models import User

from Accounts.models import Profile

# Register your models here.

admin.register([Profile, User])