import uuid

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


class Category(models.Model):
    ''' A category of FlashCards e.g. Spanish'''

    name = models.CharField(max_length=50,
                            help_text='Name of category.')
    created_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)

    def __str__(self):
        return self.name


class FlashCard(models.Model):
    ''' Represents a single flash card.'''

    LEVELS = tuple((x, x) for x in range(1, 11))

    TYPES = (
        ('s', 'Short'),
        ('l', 'Long'),
    )

    COLOURS = {
        1: '#d7ffbb',  # green
        2: '#AAFFEE',  # aqua
        3: '#cfe3ff',  # blue
        4: '#d4d0ff',  # lilac
        5: '#ffc0cb',  # pink
        6: '#ff7169',  # red
        7: '#FFD394',  # orange
        8: '#FDFD96',  # yellow
        9: '#FFFFFF',  # white
        10: '#c0c0c0'  # silver
    }

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
    image = models.ImageField(upload_to='tmp/',
                              blank=True,
                              null=True,
                              help_text='image representation of the question.')
    audio = models.FileField(upload_to='tmp/',
                             blank=True,
                             null=True,
                             help_text='audio representation of the question.')
    level = models.IntegerField(choices=LEVELS,
                                help_text='difficulty level.')
    colour = models.CharField(max_length=20,
                              null=True,
                              blank=True,
                              help_text='colour of flash card.')
    type = models.CharField(
        max_length=20,
        choices=TYPES,
        help_text='short or long charactered card.'
    )

    def __str__(self):
        return f'{self.pk}'

    def save(self, *args, **kwargs):
        # set colour based upon level
        colour = self.COLOURS.get(int(self.level))
        self.colour = colour
        super().save(self, *args, **kwargs)


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
    date = models.DateTimeField(null=True, blank=True, default=timezone.now())
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
        return f'{self.participant.username} - {self.date}'
