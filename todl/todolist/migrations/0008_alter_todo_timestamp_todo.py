# Generated by Django 4.0.4 on 2022-06-01 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0007_rename_todo_todo_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='timestamp_todo',
            field=models.DateField(),
        ),
    ]
