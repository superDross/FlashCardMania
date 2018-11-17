from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    ''' A category of FlashCards e.g. Spanish'''

    name = models.CharField(max_length=50,
                            help_text='Name of category.')

    def __str__(self):
        return self.name


class FlashCard(models.Model):
    ''' Represents a single flash card.'''

    LEVELS = tuple((x, x) for x in range(1, 101))
    TYPES = (
        ('s', 'Short'),
        ('l', 'Long'),
    )

    created_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 help_text='category in which the flash card belongs.')
    image = models.ImageField(upload_to='image_files/',
                              help_text='image representation of the question.')
    audio = models.FileField(upload_to='audio_files/',
                             help_text='audio representation of the question.')
    level = models.IntegerField(choices=LEVELS,
                                help_text='difficulty level.')
    type = models.CharField(
        max_length=20,
        choices=TYPES,
        blank=True,
        help_text='short or long charactered card.'
    )

    def __str__(self):
        return self.pk
