# Generated by Django 5.0 on 2023-12-21 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lneedapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='username',
            field=models.CharField(default=True, max_length=150),
        ),
    ]
