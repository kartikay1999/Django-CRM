# Generated by Django 3.1.6 on 2021-02-07 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0003_auto_20210207_0255'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_agent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_organiser',
            field=models.BooleanField(default=True),
        ),
    ]
