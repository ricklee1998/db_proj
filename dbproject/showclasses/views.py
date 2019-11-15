from django.shortcuts import render
from django.db import connection
from .models import Classes
def class_sql(self):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM Classes")
    row = cursor.fetchall()
    return row

def show_sql(request):
    
    row = class_sql(Classes)

    return render(request, 'showclasses/classes.html', {"row": row})