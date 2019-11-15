from django.shortcuts import render, redirect
from django.db import connection
from .models import Users
from .models import Classes

# def class_sql(self):
#     cursor = connection.cursor()
#     cursor.execute("SELECT name FROM Classes")
#     row = cursor.fetchall()
#     return row

# def show_sql(request):
    
#     row = class_sql(Classes)

#     return render(request, 'showclasses/index.html', {"row": row})

def confirm(self, username, passwd):
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, email, password FROM Users WHERE email = %s and password = %s", [username, passwd])
    row = cursor.fetchall()
    return row


def login(request):
    if request.method == "POST":
        username = request.POST['loginid']
        password = request.POST['loginpw']
        permit = confirm(Users, username, password)
        if (permit is not None):
            id = permit[0][0]
            return redirect(str(id) + '/teacherpage')
        else:
            return render(request, 'main/login.html')
    else:
        return render(request, 'main/login.html')

def get_madeclass(self1, self2, id):
    cursor = connection.cursor()
    cursor.execute("SELECT Classes.name FROM Users INNER JOIN Classes ON Users.user_id = Classes.master_id WHERE user_id =%s", [id])
    row = cursor.fetchall()
    return row


def mypage_t(request, id):
    class_name = get_madeclass(Users, Classes, id)
    return render(request, 'main/a.html', {"class_name": class_name})
# def mypage_t(request):
#     if:

#     else:
