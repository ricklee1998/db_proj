from django.forms import ModelForm
from .models import *

class Form(ModelForm):
    class Meta:
        model = Classes
        fields = ['name', 'capacity', 'master']
class lectureForm(ModelForm):
    class Meta:
        model = Lectures
        fields = ['name', 'start_time', 'end_time']
class questionForm(ModelForm):
    class Meta:
        model = Questions
        fields = ['type', 'question', 'bogi', 'answer', 'difficulty', 'real_difficulty']
class lkForm(ModelForm):
    class Meta:
        model = LectureKeywords
        fields = ['keyword', 'weight']