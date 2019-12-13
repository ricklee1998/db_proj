from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db import connection
from .models import *
from .forms import *
from random import *
from decimal import *
import csv, io
# 아이디 비번 확인
def confirm(self, username, passwd):
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, email, password, type FROM users WHERE email = %s and password = %s", [username, passwd])
    row = cursor.fetchone()
    return row


# 로그인
def login(request):
    if request.method == "POST":
        username = request.POST['loginid']
        password = request.POST['loginpw']
        permit = confirm(Users, username, password)
        if (permit is not None):
            id = permit[0]
            usertype = permit[3]
            if(str(usertype)=="0"):
            	return redirect(str(id) + '/studentpage')
            elif(str(usertype)=="1"):
            	return redirect(str(id) + '/teacherpage')
        else:
            return render(request, 'main/login.html')
    else:
        return render(request, 'main/login.html')
# 강사가 만든 과목 가져오기
def get_madeclass(self1, self2, id):
    cursor = connection.cursor()
    cursor.execute("SELECT classes.name, classes.class_id, classes.capacity FROM users INNER JOIN classes ON users.user_id = classes.master_id WHERE user_id =%s", [id])
    row = cursor.fetchall()
    return row

# 강사 과목 페이지
def mypage_t(request, id):
    if request.method == "POST" and 'class_add' in request.POST:
        return redirect('./writeclass')
    elif request.method == "POST" and 'delete' in request.POST:
        class_id = request.POST['delete']
        cursor = connection.cursor()
        cursor.execute("DELETE FROM classes WHERE class_id = %s", [class_id])
        class_name = get_madeclass(Users, Classes, id)
        return render(request, 'main/classes.html', {"class_name": class_name})
    else:
        class_name = get_madeclass(Users, Classes, id)
        return render(request, 'main/classes.html', {"class_name": class_name})
# 과목만들기
def writeclass(request, teacher_id):
    if request.method == 'POST':
        form = Form(request.POST)
        cursor = connection.cursor()
        cursor.execute("SELECT max(class_id) class_id FROM classes")
        row = cursor.fetchone()
        if (row[0] is not None):
            newid = row[0]+1
        else:
            newid = 0
        if form.is_valid():
            name = form.cleaned_data['name']
            capacity = form.cleaned_data['capacity']
            master= form.cleaned_data['master']
            if (master.user_id == teacher_id):
                cursor = connection.cursor()
                cursor.execute("INSERT INTO classes VALUES (%s, %s, %s, %s)", [newid, name, capacity, master.user_id])
                return redirect(mypage_t, master.user_id)
    else:
        form = Form()
    return render(request, 'main/writeclass.html', {"form": form})
#과목안에 포함된 강의 가져오기
def get_lecturename(Users, Classes, Lectures, teacher_id, class_id):
    cursor = connection.cursor()
    cursor.execute("SELECT Lectures.name, Lectures.lecture_id FROM users, Classes, Lectures WHERE users.user_id = %s and Classes.class_id = %s and users.user_id = Classes.master_id and Classes.class_id = Lectures.class_id", [teacher_id, class_id])
    row = cursor.fetchall()
    return row
#강의 페이지
def lecture(request, teacher_id, class_id):
    if request.method == "POST" and 'lecture_add' in request.POST:
        return redirect('./writelecture')
    elif request.method == "POST" and 'delete' in request.POST:
        lecture_id = request.POST['delete']
        cursor = connection.cursor()
        cursor.execute("DELETE FROM lectures WHERE lecture_id = %s", [lecture_id])
        lecture_name = get_lecturename(Users, Classes, Lectures, teacher_id, class_id)
        return render(request, 'main/lecture.html', {"lecture_name": lecture_name})
    else:
        lecture_name = get_lecturename(Users, Classes, Lectures, teacher_id, class_id)
        return render(request, 'main/lecture.html', {"lecture_name": lecture_name})
#강의 쓰기
def writelecture(request, teacher_id, class_id):
    if request.method == 'POST':
        form = lectureForm(request.POST)
        cursor = connection.cursor()
        cursor.execute("SELECT max(lecture_id) FROM lectures")
        row = cursor.fetchone()
        if (row[0] is not None):
            newid = row[0]+1
        else:
            newid = 1
        if form.is_valid():
            name = form.cleaned_data['name']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            if (start_time < end_time):
                cursor = connection.cursor()
                cursor.execute("INSERT INTO lectures VALUES (%s, %s, %s, %s, %s)", [newid, name, start_time, end_time, class_id])
                return redirect(lecture, teacher_id, class_id)
            else:
                return redirect(writelecture, teacher_id, class_id)
            
    else:
        form = lectureForm()
    return render(request, 'main/writelecture.html', {"form": form})
#문제 id가져오기
def get_questionid(Users, Classes, Lectures, Questions, teacher_id, class_id, lecture_id):
    cursor = connection.cursor()
    cursor.execute("SELECT Questions.question_id, question, questions.type FROM Users, Classes, Lectures, Questions WHERE Users.user_id = Classes.master_id and Classes.class_id = Lectures.class_id and Lectures.lecture_id = Questions.lecture_id and Users.user_id = %s and Lectures.class_id = %s and Questions.lecture_id = %s",[teacher_id, class_id, lecture_id])
    row = cursor.fetchall()
    return row
#문제페이지
def question(request, teacher_id, class_id, lecture_id):
    if request.method == "POST" and 'addquestion' in request.POST:
        return redirect('./addquestion')
    elif request.method == "POST" and 'add_keywords' in request.POST:
        return redirect('./addkeyword')
    elif request.method == "POST" and 'questionbank' in request.POST:
        return redirect('./questionbank')
    elif request.method == "POST" and 'delete' in request.POST:
        question_id = request.POST['delete']
        cursor = connection.cursor()
        cursor.execute("DELETE FROM questions WHERE question_id = %s", [question_id])
        cursor = connection.cursor()
        cursor.execute("SELECT question_id, keyword FROM question_keywords WHERE lecture_id = %s", [lecture_id])
        keywords = cursor.fetchall()
        question_id = get_questionid(Users, Classes, Lectures, Questions, teacher_id, class_id, lecture_id)
        return render(request, 'main/question.html', {"question_id": question_id, "keywords":keywords})
    elif request.method == "POST" and 'showlog' in request.POST:
        question_id = request.POST['showlog']
        cursor = connection.cursor()
        cursor.execute("select count(*), sum(score) FROM student_question_log where question_id = %s", [question_id])
        log = cursor.fetchone()
        if (log[0] != 0):
            cursor = connection.cursor()
            cursor.execute("SELECT sum(score_portion) FROM questions as qb natural JOIN question_keywords where qb.question_id = %s group by qb.question_id", [question_id])
            score = cursor.fetchone()
            score = str(score[0])
            student_num = log[0]
            sum_score = str(log[1])
            real_difficulty =  10-((int(sum_score) / (int(student_num) * int(score))) * 10)
            cursor.execute("update questions set real_difficulty = %s WHERE question_id = %s", [real_difficulty, question_id])
            real_difficulty = (10 -real_difficulty)*10
            return redirect(show_log, teacher_id, class_id, lecture_id, real_difficulty, question_id)
        else:
            return redirect(show_log, teacher_id, class_id, lecture_id, "None", question_id)
    elif request.method == "POST" and 'add_to_bank' in request.POST:
        question_id = request.POST['add_to_bank']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM questions, question_keywords WHERE questions.question_id = question_keywords.question_id and questions.question_id = %s", [question_id])
        exist = cursor.fetchone()
        if (exist is not None):
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM questions WHERE question_id = %s", [question_id])
            question = cursor.fetchone()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM question_keywords WHERE question_id = %s",[question_id])
            question_keyw = cursor.fetchall()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM question_parameter WHERE question_id = %s", [question_id])
            question_par = cursor.fetchall()
            cursor = connection.cursor()
            cursor.execute("SELECT max(questionbank_id) FROM question_bank")
            maxid = cursor.fetchone()
            if (maxid[0] is not None):
                newid = maxid[0] +1
            else:
                newid = 1
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM question_bank")
            question_b = cursor.fetchall()
            for item_q in question_b:
                if (item_q[1]==question[1] and item_q[2]==question[2] and item_q[3]==question[3] and item_q[4]==question[4] and item_q[5]==question[5] and question[7]==lecture_id):
                    cursor = connection.cursor()
                    cursor.execute("delete FROM question_bank WHERE questionbank_id = %s", [item_q[0]])
            cursor = connection.cursor()
            cursor.execute("INSERT INTO question_bank VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [newid, question[1], question[2], question[3], question[4], question[5], question[6], teacher_id])
            for item in question_keyw:
                cursor = connection.cursor()
                cursor.execute("SELECT max(id) FROM question_keywords_bank")
                maxid = cursor.fetchone()
                if (maxid[0] is not None):
                    newid_k = maxid[0] +1
                else:
                    newid_k = 1
                cursor = connection.cursor()
                cursor.execute("INSERT INTO question_keywords_bank VALUES (%s, %s, %s, %s)", [newid_k, item[1], item[3], newid])
            if (question_par is not None):
                for item in question_par:
                    cursor = connection.cursor()
                    cursor.execute("SELECT max(id) FROM question_parameter_bank")
                    maxid = cursor.fetchone()
                    if (maxid[0] is not None):
                        newid_p = maxid[0] +1
                    else:
                        newid_p = 1
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO question_parameter_bank VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", [newid_p, item[1], item[2], item[3], item[4], item[5], item[6], newid, item[0]])
            cursor = connection.cursor()
            cursor.execute("SELECT question_id, keyword FROM question_keywords WHERE lecture_id = %s", [lecture_id])
            keywords = cursor.fetchall()
            question_id = get_questionid(Users, Classes, Lectures, Questions, teacher_id, class_id, lecture_id)
            return render(request, 'main/question.html', {"question_id": question_id, "keywords":keywords})
        else:
            cursor = connection.cursor()
            cursor.execute("SELECT question_id, keyword FROM question_keywords WHERE lecture_id = %s", [lecture_id])
            keywords = cursor.fetchall()
            question_id = get_questionid(Users, Classes, Lectures, Questions, teacher_id, class_id, lecture_id)
            return render(request, 'main/question.html', {"question_id": question_id, "keywords":keywords})
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT question_id, keyword FROM question_keywords WHERE lecture_id = %s", [lecture_id])
        keywords = cursor.fetchall()
        question_id = get_questionid(Users, Classes, Lectures, Questions, teacher_id, class_id, lecture_id)
        return render(request, 'main/question.html', {"question_id": question_id, "keywords":keywords})

#파일 업로드
def upload(request, teacher_id, class_id, lecture_id, question_id):
    if request.method == "POST" and 'select' in request.POST :
        csv_file = request.FILES['file222']
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=','):
            cursor = connection.cursor()
            cursor.execute("SELECT max(id) FROM question_parameter")
            row = cursor.fetchone()
            if (row[0] is not None):
                newid = row[0] +1
            else:
                newid = 1
            cursor = connection.cursor()
            for i in range(len(column)):
                if column[i] == '':
                    column[i] = 0
            cursor.execute("INSERT INTO question_parameter VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", [column[0], column[1], column[2], column[3], column[4], column[5], column[6], newid, question_id])
        return redirect('../question')
    return render(request, 'main/upload.html')
#로그 페이지
def show_log(request, teacher_id, class_id, lecture_id, real_difficulty, question_id):
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, score FROM student_question_log WHERE question_id = %s", [question_id])
    row = cursor.fetchall()
    return render(request, 'main/log.html', {"avg":real_difficulty, "log":row})
#문제 만들기
def writequestion(request, teacher_id, class_id, lecture_id):
    if request.method == 'POST':
        form = questionForm(request.POST)
        cursor = connection.cursor()
        cursor.execute("SELECT max(question_id) FROM questions")
        row = cursor.fetchone()
        if (row[0] is not None):
            newid = row[0] +1
        else:
            newid = 1
        if form.is_valid():
            types = form.cleaned_data['type']
            questions = form.cleaned_data['question']
            bogi = form.cleaned_data['bogi']
            answer = form.cleaned_data['answer']
            difficult = form.cleaned_data['difficulty']
            real_difficulty = form.cleaned_data['real_difficulty']
            cursor = connection.cursor()
            cursor.execute("INSERT INTO questions VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [newid, types, questions, bogi, answer, difficult, real_difficulty, lecture_id])
            return redirect(question, teacher_id, class_id, lecture_id)
    else:
        form = questionForm()
        return render(request, 'main/writequestion.html', {"form":form})
#문제 추출하기
def get_sets(q_number, avg, score, keyword):
        int_q_number = int(q_number)
        keyword_list = keyword.split()
        keyword_num = len(keyword_list)
        if (keyword_num == 1):
            cursor = connection.cursor()
            cursor.execute("create view test as select qb.questionbank_id, qb.difficulty, sum(score_portion) as score, qb.real_difficulty FROM question_bank as qb natural join question_keywords_bank WHERE EXISTS (select * from users where keyword = %s) group by questionbank_id", [keyword_list[0]])
        elif (keyword_num == 2):
            cursor = connection.cursor()
            cursor.execute("create view test as select qb.questionbank_id, qb.difficulty, sum(score_portion) as score, qb.real_difficulty FROM question_bank as qb natural join question_keywords_bank WHERE EXISTS (select * from users where keyword = %s or keyword = %s) group by questionbank_id", [keyword_list[0], keyword_list[1]])
        elif (keyword_num == 3):
            cursor = connection.cursor()
            cursor.execute("create view test as select qb.questionbank_id, qb.difficulty, sum(score_portion) as score, qb.real_difficulty FROM question_bank as qb natural join question_keywords_bank WHERE EXISTS (select * from users where keyword = %s or keyword = %s or keyword = %s) group by questionbank_id", [keyword_list[0], keyword_list[1], keyword_list[2]])
        elif (keyword_num == 4):
            cursor = connection.cursor()
            cursor.execute("create view test as select qb.questionbank_id, qb.difficulty, sum(score_portion) as score, qb.real_difficulty FROM question_bank as qb natural join question_keywords_bank WHERE EXISTS (select * from users where keyword = %s or keyword = %s or keyword = %s or keyword = %s) group by questionbank_id", [keyword_list[0], keyword_list[1], keyword_list[2], keyword_list[3]])
        cursor = connection.cursor()
        cursor.execute("create view test1 as select * from test order by rand() limit %s", [int_q_number])
        cri = True
        while(cri):
            cursor = connection.cursor()
            cursor.execute("select * from test1")
            row = cursor.fetchall()
            diff = [item[1] for item in row]
            getavg = 0
            for diff1 in diff:
                getavg = getavg+diff1
            getavg = getavg/int_q_number
            sco = [item[2] for item in row]
            getscore = 0
            for sco1 in sco:
                getscore = getscore + int(sco1)
            if (getavg >= int(avg) and getavg<int(avg)+1 and getscore >= int(score)-5 and getscore <= int(score)+5):
                cri = False
        cursor = connection.cursor()
        cursor.execute("drop view test")
        cursor = connection.cursor()
        cursor.execute("drop view test1")
        return row
#문제은행
def show_questionbank(request, teacher_id, class_id, lecture_id):
    if request.method == 'POST':
        return redirect(show_extracted, teacher_id, class_id, lecture_id)
    else:
        cursor = connection.cursor()
        cursor.execute("select difficulty, sum(score_portion), question_bank.questionbank_id  from question_bank, question_keywords_bank WHERE question_bank.questionbank_id = question_keywords_bank.questionbank_id group by question_bank.questionbank_id")
        row = cursor.fetchall()
        cursor = connection.cursor()
        cursor.execute("select question_bank.questionbank_id, keyword FROM question_bank, question_keywords_bank WHERE question_bank.questionbank_id = question_keywords_bank.questionbank_id")
        row1 = cursor.fetchall()
        return render(request, 'main/questionbank.html', {"question_info": row, "keywords_info": row1})
#추출된 문제 페이지
def show_extracted(request, teacher_id, class_id, lecture_id):
    if request.method == 'POST' and 'select' in request.POST :
        q_number = request.POST['qnum']
        avg = request.POST['avg']
        score = request.POST['score']
        keyword = request.POST['keyword']
        if (q_number != '' and avg != '' and score != '' and keyword != ''):
            row = get_sets(q_number, avg, score, keyword)
            temp = ((q_number, avg, score, keyword),)
            return redirect(show_extractednext, teacher_id, class_id, lecture_id, q_number, avg, score, keyword)
        else:
            return render(request, 'main/extractquestion.html')
    else:
        return render(request, 'main/extractquestion.html')
#다음추출문제
def show_extractednext(request, teacher_id, class_id, lecture_id, q_number, avg, score, keyword):
    if request.method == 'POST' and 'nextextract' in request.POST :
        row = get_sets(q_number, avg, score, keyword)
        return render(request, 'main/extractquestion.html', {"set": row})
    elif request.method == 'POST' and 'banktoquestion' in request.POST:
        questionbank_id = request.POST['bankbank']
        questionbank_id_list = questionbank_id.split(',')
        questionbank_id_list.remove('')
        for questionbank_id in questionbank_id_list:
            cursor = connection.cursor()
            cursor.execute("SELECT max(question_id) FROM questions")
            maxid = cursor.fetchone()
            if (maxid[0] is not None):
                newid = maxid[0] +1
            else:
                newid = 1
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM question_bank WHERE questionbank_id = %s", [questionbank_id])
            row = cursor.fetchall()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO questions VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [newid, row[0][1], row[0][2],row[0][3],row[0][4],row[0][5],row[0][6],lecture_id])

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM question_keywords_bank WHERE questionbank_id = %s", [questionbank_id])
            row = cursor.fetchall()
            for item in row:
                cursor = connection.cursor()
                cursor.execute("SELECT max(id) FROM question_keywords")
                maxid = cursor.fetchone()
                if (maxid[0] is not None):
                    newid1 = maxid[0] +1
                else:
                    newid1 = 1
                cursor = connection.cursor()
                cursor.execute("INSERT INTO question_keywords VALUES (%s, %s, %s, %s, %s)", [newid1, item[1], lecture_id, item[2], newid])
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM question_parameter_bank WHERE questionbank_id = %s", [questionbank_id])
            row=  cursor.fetchall()
            for item in row:
                cursor = connection.cursor()
                cursor.execute("SELECT max(id) FROM question_parameter")
                maxid = cursor.fetchone()
                if (maxid[0] is not None):
                    newid1 = maxid[0] +1
                else:
                    newid1 = 1
                cursor = connection.cursor()
                cursor.execute("INSERT INTO question_parameter VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", [item[8], item[1], item[2],item[3],item[4],item[5], item[6], newid1, newid])
        return redirect(question, teacher_id, class_id, lecture_id)
    else:
        row = get_sets(q_number, avg, score, keyword)
        return render(request, 'main/extractquestion.html', {"set": row})
#강의에 키워드 추가
def addkeyword(request, teacher_id, class_id, lecture_id):
    if request.method == 'POST':
        form = lkForm(request.POST)
        cursor = connection.cursor()
        cursor.execute("SELECT max(id) FROM lecture_keywords")
        row = cursor.fetchone()
        if (row[0] is not None):
            newid = row[0] +1
        else:
            newid = 1
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            weight = form.cleaned_data['weight']
            cursor = connection.cursor()
            cursor.execute("INSERT INTO lecture_keywords VALUES (%s, %s, %s, %s)", [newid, keyword, weight, lecture_id])
            return redirect(question, teacher_id, class_id, lecture_id)
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT keyword, weight FROM lectures, lecture_keywords WHERE lectures.lecture_id = lecture_keywords.lecture_id and lectures.lecture_id = %s", [lecture_id])
        row = cursor.fetchall()
        form = lkForm()
        return render(request, 'main/addkeyword.html', {"form":form, "row": row})
#문제에 키워드 추가
def addkeyword_toquestion(request, teacher_id, class_id, lecture_id, question_id):
    if request.method == "POST":
        keyword = request.POST['keyword']
        score = request.POST['score']
        try:
            if (int(score)>0):
                cursor = connection.cursor()
                cursor.execute("SELECT keyword FROM lectures, lecture_keywords WHERE lectures.lecture_id = lecture_keywords.lecture_id and lectures.lecture_id = %s", [lecture_id])
                row = [item[0] for item in cursor.fetchall()]
                if (keyword in row):
                    cursor = connection.cursor()
                    cursor.execute("SELECT keyword From question_keywords WHERE question_id = %s", [question_id])
                    inkeyword = [initem[0] for initem in cursor.fetchall()]
                    if (keyword in inkeyword):
                        cursor = connection.cursor()
                        cursor.execute("SELECT keyword, weight FROM lectures, lecture_keywords WHERE lectures.lecture_id = lecture_keywords.lecture_id and lectures.lecture_id = %s ", [lecture_id])
                        keywords = cursor.fetchall()
                        return render(request, 'main/addkeywords_toquestion.html', {"keywords":keywords})
                    cursor = connection.cursor()
                    cursor.execute("SELECT max(id) FROM question_keywords")
                    maxid = cursor.fetchone()
                    if (maxid[0] is not None):
                        newid = maxid[0]+1
                    else:
                        newid = 1
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO question_keywords VALUES (%s, %s, %s, %s, %s)", [newid, keyword, lecture_id, score, question_id])
                    return redirect(question, teacher_id, class_id, lecture_id)
                else:
                    cursor = connection.cursor()
                    cursor.execute("SELECT keyword, weight FROM lectures, lecture_keywords WHERE lectures.lecture_id = lecture_keywords.lecture_id and lectures.lecture_id = %s ", [lecture_id])
                    keywords = cursor.fetchall()
                    return render(request, 'main/addkeywords_toquestion.html', {"keywords":keywords})
        except ValueError:
            cursor = connection.cursor()
            cursor.execute("SELECT keyword, weight FROM lectures, lecture_keywords WHERE lectures.lecture_id = lecture_keywords.lecture_id and lectures.lecture_id = %s ", [lecture_id])
            keywords = cursor.fetchall()
            return render(request, 'main/addkeywords_toquestion.html', {"keywords":keywords})
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT keyword, weight FROM lectures, lecture_keywords WHERE lectures.lecture_id = lecture_keywords.lecture_id and lectures.lecture_id = %s ", [lecture_id])
        keywords = cursor.fetchall()
        return render(request, 'main/addkeywords_toquestion.html', {"keywords":keywords})
# 학생 페이지
def mypage_s(request, id):
    if request.method == "POST":
        return redirect('./classlist')
    else:
        class_name = get_stuclass(Users, UserClasses, Classes, id)
        return render(request, 'main/stu_classes.html', {"class_name": class_name})

# DB 학생 과목 가져오기
def get_stuclass(self1, self2, self3, id):
    cursor = connection.cursor()
    cursor.execute("SELECT classes.name, classes.class_id, classes.capacity, classes.master_id FROM user_classes INNER JOIN classes ON user_classes.class_id=classes.class_id WHERE user_classes.user_id =%s", [id])
    row = cursor.fetchall()
    return row

# 현재수강인원조회
def get_curstu(class_id):
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM user_classes WHERE role = 0 and class_id = %s", [class_id])
    row = cursor.fetchone()
    return row[0]

# 각 과목 수강인원조회
def get_countclass():
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM classes")
    row = cursor.fetchone()
    return row[0]

# 수강편람조회 및 수강신청
def callofallclasses(request, student_id):
    class_name = get_allclass(Users, id)
    count_class = get_countclass()
    cur_cur_stu=(())
    for j in range(0, count_class):
        temp = ((get_curstu(j),class_name[j][0]),)
        cur_cur_stu = cur_cur_stu + temp
    if request.method == "POST":
        the_classid = request.POST['class_app']
        cursor = connection.cursor()
        cursor.execute("SELECT class_id FROM user_classes WHERE user_id = %s", [student_id])
        class_list = cursor.fetchall()
        alreadyin = 0
        for inclass in class_list:
            if int(the_classid) == inclass[0]:
                alreadyin = 1
        if alreadyin == 1:
            return redirect('./studentpage', student_id)
        else:
            cur_stu = get_curstu(the_classid)
            cursor = connection.cursor()
            cursor.execute("SELECT capacity FROM classes WHERE class_id = %s", [the_classid])
            row = cursor.fetchone()
            capacity = row[0]
            cursor = connection.cursor()
            cursor.execute("SELECT max(user_class_id) FROM user_classes")
            getid = cursor.fetchall()
            if (getid[0][0] is not None):
                newid = getid[0][0]+1
            else:
                newid = 1
            if (cur_stu < capacity):
                cursor = connection.cursor()
                cursor.execute("INSERT INTO user_classes VALUES (%s, %s, %s, %s)", [newid, "0", the_classid, student_id])
                return redirect('./studentpage', student_id)
            else:
                return redirect('./studentpage', student_id)
    
    return render(request, 'main/classeslist.html', {"class_name": class_name, "cur_cur_stu":cur_cur_stu})
    
# DB 모든 과목 가져오기
def get_allclass(self1, id):
    cursor = connection.cursor()
    cursor.execute("SELECT name, class_id, capacity, master_id FROM classes")
    row = cursor.fetchall()
    return row

# 학생 강의 페이지
def stulecture(request, student_id, class_id):
    lecture_name = get_stulecture(Classes, Lectures, student_id, class_id)
    return render(request, 'main/stu_lectures.html', {"lecture_name": lecture_name})

# DB 학생 강의 가져오기
def get_stulecture(Classes, Lectures, student_id, class_id):
    cursor = connection.cursor()
    cursor.execute("SELECT lectures.name, lectures.lecture_id, lectures.start_time, lectures.end_time FROM classes, lectures WHERE classes.class_id = %s and classes.class_id = lectures.class_id", [class_id])
    row = cursor.fetchall()
    return row

# 학생 문제 페이지
def stuquestion(request, student_id, class_id, lecture_id):
    question_id = get_stuquestion(Users, Classes, Lectures, Questions, student_id, class_id, lecture_id)
    return render(request, 'main/stu_questions.html', {"question_id": question_id})

# DB 학생 문제 가져오기
def get_stuquestion(Users, Classes, Lectures, Questions, student_id, class_id, lecture_id):
    cursor = connection.cursor()
    cursor.execute("SELECT questions.question_id, questions.question, questions.type, questions.bogi FROM questions WHERE EXISTS (SELECT * FROM question_keywords WHERE questions.question_id = question_keywords.question_id) and questions.lecture_id = %s",[lecture_id])
    row = cursor.fetchall()
    return row

# DB 학생 문제풀기 가져오기
def show_stuquestion(Users, Classes, Lectures, Questions, student_id, class_id, lecture_id, question_id):
    cursor = connection.cursor()
    cursor.execute("SELECT questions.question_id, questions.question, questions.type, questions.bogi, questions.answer FROM users, classes, lectures, questions WHERE classes.class_id = lectures.class_id and lectures.lecture_id = questions.lecture_id and users.user_id = %s and lectures.class_id = %s and questions.lecture_id = %s and questions.question_id = %s",[student_id, class_id, lecture_id, question_id])
    row = cursor.fetchall()
    return row

# DB 학생 파라미터 가져오기
def show_parameter(Users, Classes, Lectures, Questions, QuestionParameter, student_id, class_id, lecture_id, question_id, rnd_num):
    cursor = connection.cursor()
    cursor.execute("SELECT question_parameter.key_value, question_parameter.pr1, question_parameter.pr2, question_parameter.pr3, question_parameter.pr4, question_parameter.pr5, question_parameter.answer FROM users, classes, lectures, questions, question_parameter WHERE classes.class_id = lectures.class_id and lectures.lecture_id = questions.lecture_id and questions.question_id = question_parameter.question_id and users.user_id = %s and lectures.class_id = %s and questions.lecture_id = %s and question_parameter.key_value= %s and questions.question_id = %s",[student_id, class_id, lecture_id, rnd_num, question_id])
    row = cursor.fetchall()
    return row

# DB 학생 문제들 배점 가져오기
def get_scoreportion(question_id):
    cursor = connection.cursor()
    cursor.execute("SELECT qb.question_id, sum(score_portion) FROM questions as qb natural JOIN question_keywords group by qb.question_id")
    row = cursor.fetchall()
    return row

# DB 파라미터 카운트
def count_parameter(Users, Classes, Lectures, Questions, QuestionParameter, student_id, class_id, lecture_id, question_id):
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM users, classes, lectures, questions, question_parameter WHERE classes.class_id = lectures.class_id and lectures.lecture_id = questions.lecture_id and questions.question_id = question_parameter.question_id and users.user_id = %s and lectures.class_id = %s and questions.lecture_id = %s and questions.question_id = %s",[student_id, class_id, lecture_id, question_id])
    row = cursor.fetchall()
    return row

# 학생 문제풀기 페이지
def stusolve(request, student_id, class_id, lecture_id, question_id):
    if request.method == "POST":
        userans = request.POST['ans_ans']
        tchans = request.POST['ans_teacher']
        scoreans = request.POST['ans_score']
        if(userans.isnumeric() and tchans.isnumeric()):
            var1 = float(userans)
            var2 = float(tchans)
        else:
            var1 = userans
            var2 = tchans
        cursor = connection.cursor()
        cursor.execute("SELECT max(id) FROM Student_Question_Log")
        maxid = cursor.fetchone()
        if (maxid[0] is not None):
            newid = maxid[0]+1
        else:
            newid = 1
        curosr = connection.cursor()
        cursor.execute("select * FROM Student_Question_Log WHERE question_id = %s and user_id = %s", [question_id, student_id])
        row = cursor.fetchone()
        if (row is not None):
            if var1 == var2 :
                cursor = connection.cursor()
                cursor.execute("UPDATE Student_Question_Log SET score = %s WHERE question_id = %s and user_id = %s", [scoreans, question_id, student_id])
            else:
                zero = '0'
                cursor = connection.cursor()
                cursor.execute("UPDATE Student_Question_Log SET score = %s WHERE question_id = %s and user_id = %s", [zero, question_id, student_id])
        else:
            if var1 == var2 :
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Student_Question_Log VALUES (%s, %s, %s, %s)", [newid, scoreans, question_id, student_id])    
            else:
                zero = '0'
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Student_Question_Log VALUES (%s, %s, %s, %s)", [newid, zero, question_id, student_id]) 
        return redirect(stuquestion, student_id, class_id, lecture_id)
        #return redirect(student_id, class_id, lecture_id)
    else:
        rnd_count = count_parameter(Users, Classes, Lectures, Questions, QuestionParameter, student_id, class_id, lecture_id, question_id)
        if(rnd_count[0][0]>0):
       #문제 유형 type2
            rnd_num = randrange(rnd_count[0][0])+1
            parameter_id = show_parameter(Users, Classes, Lectures, Questions, QuestionParameter, student_id, class_id, lecture_id, question_id, rnd_num)
            problem_id = show_stuquestion(Users, Classes, Lectures, Questions, student_id, class_id, lecture_id, question_id)
            score_id = get_scoreportion(question_id)
            return render(request, 'main/stu_problems.html', {"problem_id": problem_id, "parameter_id": parameter_id, "score_id": score_id})
        else:
       #문제 유형 type0, 1
            problem_id = show_stuquestion(Users, Classes, Lectures, Questions, student_id, class_id, lecture_id, question_id)
            score_id = get_scoreportion(question_id)
            return render(request, 'main/stu_problems.html', {"problem_id": problem_id, "score_id": score_id})
