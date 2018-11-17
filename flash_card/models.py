from django.contrib.auth.models import User
from django.db import models


class FlashCard(models.Model):
    ''' Represents a single flash card.'''

    LEVELS = tuple((x, x) for x in range(1, 101))

    created_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='image_files/')
    audio = models.FileField(upload_to='audio_files/')
    level = models.IntegerField(choices=LEVELS)

    def __str__(self):
        return self.pk
