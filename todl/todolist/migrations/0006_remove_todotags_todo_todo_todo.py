# Generated by Django 4.0.4 on 2022-05-25 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0005_todotags_todo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todotags',
            name='todo',
        ),
        migrations.AddField(
            model_name='todo',
            name='todo',
            field=models.ManyToManyField(to='todolist.todotags'),
        ),
    ]
