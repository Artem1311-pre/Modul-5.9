# Generated by Django 4.2.4 on 2023-10-10 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='user',
            new_name='name',
        ),
    ]