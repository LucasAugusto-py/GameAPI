# Generated by Django 4.2.1 on 2023-09-02 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_rename_user_id_userreviews_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userreviews',
            old_name='game_id',
            new_name='game',
        ),
    ]
