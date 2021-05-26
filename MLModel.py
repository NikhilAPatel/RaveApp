import random

def ML_get_cpm(features_data):
    return 250

def ML_get_colors(features_data):
    colors=[]
    for i in range(0, 3):
        letters = '0123456789ABCDEF'
        color = ''
        for i in range(0, 6):
            color += letters[random.randint(0, 15)]
        colors.append(color)
    return colors
    