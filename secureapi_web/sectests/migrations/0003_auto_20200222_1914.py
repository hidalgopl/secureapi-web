# Generated by Django 2.0.13 on 2020-02-22 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sectests', '0002_sectestsuite_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sectest',
            options={'ordering': ('code',)},
        ),
        migrations.AlterModelOptions(
            name='sectestsuite',
            options={'ordering': ('created',)},
        ),
    ]
