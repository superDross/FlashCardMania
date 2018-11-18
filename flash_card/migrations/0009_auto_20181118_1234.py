# Generated by Django 2.1.3 on 2018-11-18 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flash_card', '0008_auto_20181118_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcard',
            name='audio',
            field=models.FileField(blank=True, help_text='audio representation of the question.', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='flashcard',
            name='image',
            field=models.ImageField(blank=True, help_text='image representation of the question.', null=True, upload_to=''),
        ),
    ]
