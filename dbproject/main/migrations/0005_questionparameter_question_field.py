# Generated by Django 2.1.7 on 2019-12-05 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_questionparameter_question_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionparameter',
            name='question_field',
            field=models.ForeignKey(db_column='question_id', default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Questions'),
            preserve_default=False,
        ),
    ]
