# Generated by Django 4.0.4 on 2022-05-24 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0004_alter_todo_body_alter_todo_title_todotags'),
    ]

    operations = [
        migrations.AddField(
            model_name='todotags',
            name='todo',
            field=models.ManyToManyField(to='todolist.todo'),
        ),
    ]
