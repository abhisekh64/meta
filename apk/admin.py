from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Campaign_id)
class Campaign_idAdmin(admin.ModelAdmin):
    list_display = ["id", "campaign_id"]
