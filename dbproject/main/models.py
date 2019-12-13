# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'users'

class Classes(models.Model):
    class_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    master = models.ForeignKey(Users, db_column='master_id', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'classes'

class UserClasses(models.Model):
    user_class_id = models.IntegerField(primary_key=True)
    role = models.CharField(max_length=255)
    class_field1 = models.ForeignKey(Classes,db_column='class_id', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, db_column='user_id', on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = 'user_classes'
        index_together = (('class_field1','user'),)


class Lectures(models.Model):
    lecture_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    class_field = models.ForeignKey(Classes, db_column='class_id', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'lectures'
        unique_together = (('lecture_id', 'class_field'),)

class LectureKeywords(models.Model):
    id = models.IntegerField(primary_key=True)
    lecture = models.ForeignKey(Lectures, db_column='lecture_id', on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    weight = models.FloatField()

    class Meta:
        managed = True
        db_table = 'lecture_keywords'

class Questions(models.Model):
    question_id = models.IntegerField(primary_key=True)
    type = models.IntegerField()
    question = models.CharField(max_length=1023)
    bogi = models.TextField(blank=True, null=True)
    answer = models.TextField()
    difficulty = models.IntegerField(blank=True, null=True)
    real_difficulty = models.IntegerField(blank=True, null=True)
    lecture = models.ForeignKey(Lectures, db_column='lecture_id', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'questions'
        unique_together = (('question_id','lecture'),)

class QuestionKeywords(models.Model):
    id = models.IntegerField(primary_key=True)
    question_field = models.ForeignKey(Questions, db_column='question_id', on_delete=models.CASCADE,)
    keyword = models.CharField(max_length=255)
    lecture_id = models.IntegerField()
    score_portion = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'question_keywords'

class QuestionParameter(models.Model):
    question_field = models.ForeignKey(Questions, db_column='question_id', on_delete=models.CASCADE)
    key_value = models.IntegerField(null=False)
    pr1 = models.FloatField(blank=True, null=True)
    pr2 = models.FloatField(blank=True, null=True)
    pr3 = models.FloatField(blank=True, null=True)
    pr4 = models.FloatField(blank=True, null=True)
    pr5 = models.FloatField(blank=True, null=True)
    answer = models.FloatField()

    class Meta:
        managed = True
        db_table = 'question_parameter'

class QuestionBank(models.Model):
    questionbank_id = models.IntegerField(primary_key=True)
    types = models.IntegerField()
    question = models.CharField(max_length=1023)
    bogi = models.TextField(blank=True, null=True)
    answer = models.TextField()
    difficulty = models.IntegerField(blank=True, null=True)
    real_difficulty = models.IntegerField(blank=True, null=True)
    teacher_field = models.ForeignKey(Users, db_column='user_id', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'question_bank'

class QuestionKeywordsBank(models.Model):
    id = models.IntegerField(primary_key = True)
    questionbank_field = models.ForeignKey(QuestionBank, db_column='questionbank_id', on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    score_portion = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'question_keywords_bank'

class QuestionParameterBank(models.Model):
    id = models.IntegerField(primary_key=True)
    key_value = models.IntegerField()
    questionbank_field = models.ForeignKey(QuestionBank, db_column='questionbank_id', on_delete=models.CASCADE)
    pr1 = models.FloatField(blank=True, null=True)
    pr2 = models.FloatField(blank=True, null=True)
    pr3 = models.FloatField(blank=True, null=True)
    pr4 = models.FloatField(blank=True, null=True)
    pr5 = models.FloatField(blank=True, null=True)
    answer = models.FloatField()
    
    class Meta:
        managed = True
        db_table = 'question_parameter_bank'

class StudentQuestionLog(models.Model):
    id = models.IntegerField(primary_key=True)
    user_field = models.ForeignKey(Users, db_column = 'user_id', on_delete=models.CASCADE)
    question_field = models.ForeignKey(Questions, db_column='question_id', on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'Student_Question_Log'