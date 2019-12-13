from django.contrib import admin
from main.models import *

class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'name', 'master')
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'password')
class LectureAdmin(admin.ModelAdmin):
    list_display = ('lecture_id', 'name', 'class_field')
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_id','lecture')
class UserClassAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'class_field1')
class QuestionParameterAdmin(admin.ModelAdmin):
    list_display = ('id', 'key_value')
# Register your models here.
admin.site.register(Users, UserAdmin)
admin.site.register(Classes, ClassAdmin)
admin.site.register(Lectures, LectureAdmin)
admin.site.register(Questions, QuestionAdmin)
admin.site.register(UserClasses, UserClassAdmin)
admin.site.register(QuestionParameter, QuestionParameterAdmin)