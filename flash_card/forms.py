from django import forms
from django.contrib.auth.models import User

from .models import Category, FlashCard


class CategoryForm(forms.Form):
    name = forms.CharField(max_length=200)
    template_name = 'flash_card/generic_form.html'


class CardForm(forms.Form):
    LEVELS = tuple((x, x) for x in range(1, 101))

    TYPES = (
        ('s', 'Short'),
        ('l', 'Long'),
    )

    question = forms.CharField(max_length=200)
    answer = forms.CharField(max_length=200)
    level = forms.ChoiceField(choices=LEVELS)
    type = forms.ChoiceField(choices=TYPES)
    image = forms.ImageField()
    audio = forms.FileField()
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    template_name = 'flash_card/creat_form.html'


class CardViewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False

    USERS = tuple((x.username, x) for x in User.objects.all())
    CATEGORIES = tuple((x.name, x) for x in Category.objects.all())

    category = forms.MultipleChoiceField(choices=CATEGORIES)
    level = forms.MultipleChoiceField(choices=FlashCard.LEVELS)
    users = forms.MultipleChoiceField(choices=USERS)
    type = forms.MultipleChoiceField(choices=FlashCard.TYPES)

    def clean(self):
        ''' If nothing selected for a field then return all for that field.'''
        d = {'category': [x.name for x in Category.objects.all()],
             'level': [x[0] for x in FlashCard.LEVELS],
             'users': [x.username for x in User.objects.all()],
             'type': [x[0] for x in FlashCard.TYPES]}
        for key, value in self.cleaned_data.items():
            if value:
                d[key] = value
        return d
