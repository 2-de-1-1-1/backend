from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Job)
admin.site.register(Company)
admin.site.register(Position)
admin.site.register(TechStack)
admin.site.register(LocationInfo)
admin.site.register(Welfare)

