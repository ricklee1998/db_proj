# Generated by Django 2.1.7 on 2019-11-25 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('class_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('capacity', models.IntegerField()),
                ('master_id', models.IntegerField()),
            ],
            options={
                'db_table': 'classes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LectureKeywords',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('lecture_id', models.IntegerField()),
                ('keyword', models.CharField(max_length=255)),
                ('weight', models.FloatField()),
            ],
            options={
                'db_table': 'lecture_keywords',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Lectures',
            fields=[
                ('lecture_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('class_id', models.IntegerField()),
            ],
            options={
                'db_table': 'lectures',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='QuestionKeywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.IntegerField()),
                ('keyword', models.CharField(max_length=255)),
                ('lecture_id', models.IntegerField()),
                ('score_portion', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'question_keywords',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('question_id', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.IntegerField()),
                ('question', models.CharField(max_length=1023)),
                ('bogi', models.TextField(blank=True, null=True)),
                ('answer', models.TextField()),
                ('difficulty', models.IntegerField(blank=True, null=True)),
                ('real_difficulty', models.IntegerField(blank=True, null=True)),
                ('lecture_id', models.IntegerField()),
            ],
            options={
                'db_table': 'questions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserClasses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=255)),
                ('class_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
            ],
            options={
                'db_table': 'user_classes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
    ]
