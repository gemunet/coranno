from django.contrib import admin

from . import models

admin.site.register(models.Dataset)
admin.site.register(models.Document)