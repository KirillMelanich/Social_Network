# Generated by Django 5.0 on 2023-12-11 17:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tweetogram", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="header",
        ),
    ]
