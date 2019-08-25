from django.contrib import admin
#We can enable our models by first importing our models from profiles_api
from profiles_api import models

# Register your models here
admin.site.register(models.UserProfile)
