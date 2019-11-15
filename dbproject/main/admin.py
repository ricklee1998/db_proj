from django.contrib import admin
from main.models import Users
from showclasses.models import Classes
class ClassAdmin(admin.ModelAdmin):
  list_display = ('class_id', 'name')
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'password')

# Register your models here.
admin.site.register(Users, UserAdmin)
admin.site.register(Classes, ClassAdmin)
