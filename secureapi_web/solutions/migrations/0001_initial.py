# Generated by Django 2.0.13 on 2019-12-25 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SecSolution',
            fields=[
                ('code', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('solution', models.TextField()),
                ('owasp_link', models.URLField()),
            ],
        ),
    ]