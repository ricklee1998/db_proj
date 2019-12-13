"""dbproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from showclasses.views import show_sql
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login),
    path('<int:teacher_id>/writeclass', writeclass),
    path('<int:id>/teacherpage', mypage_t),
    path('<int:teacher_id>/teacherpage/<int:class_id>/lecture/', lecture),
    path('<int:teacher_id>/teacherpage/<int:class_id>/lecture/writelecture', writelecture),

    path('<int:teacher_id>/teacherpage/<int:class_id>/lecture/<int:lecture_id>/question', question),
    path('<int:teacher_id>/teacherpage/<int:class_id>/lecture/<int:lecture_id>/<int:question_id>/upload', upload),
    path('<int:teacher_id>/teacherpage/<int:class_id>/lecture/<int:lecture_id>/question/<str:real_difficulty>/<str:question_id>/log', show_log),
    path('<int:teacher_id>/teacherpage/<int:class_id>/lecture/<int:lecture_id>/questionbank', show_questionbank),
    path('<int:teacher_id>/teacherpage/<int:class_id>/lecture/<int:lecture_id>/questionbank/showextracted', show_extracted),
    path('<int:teacher_id>/teacherpage/<int:class_id>/lecture/<int:lecture_id>/questionbank/showextracted/<str:q_number>/<str:avg>/<str:score>/<str:keyword>', show_extractednext),
    path('<int:teacher_id>/teacherpage/<int:class_id>/lecture/<int:lecture_id>/addquestion', writequestion),
    path('<int:teacher_id>/teacherpage/<int:class_id>/lecture/<int:lecture_id>/addkeyword', addkeyword),
    path('<int:teacher_id>/teacherpage/<int:class_id>/lecture/<int:lecture_id>/<int:question_id>/keywords', addkeyword_toquestion),
    path('teacherpage', mypage_t),
    path('classes/', show_sql),

    path('<int:id>/studentpage', mypage_s),
    path('<int:student_id>/classlist', callofallclasses),
    path('<int:student_id>/studentpage/<int:class_id>/lecture/', stulecture),
    path('<int:student_id>/studentpage/<int:class_id>/lecture/<int:lecture_id>/question', stuquestion),
    path('<int:student_id>/studentpage/<int:class_id>/lecture/<int:lecture_id>/question/<int:question_id>', stusolve),
]