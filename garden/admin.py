
# Register your models here.
from django.contrib import admin
from .models import Vegetable, WasteLog, GardenTip

admin.site.register(Vegetable)
admin.site.register(WasteLog)
admin.site.register(GardenTip)