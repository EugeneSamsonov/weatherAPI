from django.contrib import admin

from history.models import UserHistory

# Register your models here.
@admin.register(UserHistory)
class TaskAdmin(admin.ModelAdmin):
    pass