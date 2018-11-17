import uuid

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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


class GameInstance(models.Model):
    ''' Instance of a flash card game.'''

    TYPES = (
        ('c', 'Multiple Choice'),
        ('w', 'Writing')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, unique=True)
    participant = models.ForeignKey(User,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    cards = models.ManyToManyField(FlashCard,
                                   help_text='all cards used in game.')
    score = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
        help_text='percentage of correct answers in game.'
    )
    type = models.CharField(
        max_length=50,
        choices=TYPES,
        blank=True,
        help_text='type of game played'
    )

    def __str__(self):
        return f'{self.participant.username} - {self.date}, {self.time}'
