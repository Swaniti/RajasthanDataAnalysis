from django.contrib import admin
from .models import Random
from .models import DataModel
# Register your models here.
admin.site.register(Random)
admin.site.register(DataModel)