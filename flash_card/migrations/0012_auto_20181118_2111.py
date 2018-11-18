# Generated by Django 2.1.3 on 2018-11-18 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flash_card', '0011_auto_20181118_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcard',
            name='level',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], help_text='difficulty level.'),
        ),
    ]
