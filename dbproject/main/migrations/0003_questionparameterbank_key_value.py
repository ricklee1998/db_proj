# Generated by Django 2.1.7 on 2019-12-01 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_studentquestionlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionparameterbank',
            name='key_value',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
