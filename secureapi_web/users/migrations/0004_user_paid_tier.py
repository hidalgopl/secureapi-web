# Generated by Django 3.0 on 2020-06-30 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190502_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='paid_tier',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Free'), (50, 'First Tier')], default=0),
        ),
    ]
