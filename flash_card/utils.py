''' Small utility functions.'''
import random


def random_card_color(default=False):
    ''' Returns random background pastel color
        in CSS style formatting.
    '''
    colors = ['#FFB2AE', '#FDFD96', '#AAFFEE', '#FFD394']
    if default:
        color = '#FDFD96'
    else:
        color = random.choice(colors)
    css = f'background-color:{color}'
    return css

