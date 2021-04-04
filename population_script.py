import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'buyacar.settings')

import django

django.setup()
from rango.models import UserProfile, Car


def populate():

    oscar_car = [
        {'name': 'Nissan pixo 88000km', 'brand': 'Nissan', 'model': 'Pixo', 'year': 2013, 'price': 3490, 'is_new': 0,
         'other': 'Nothing'}]

    jane_car = [
        {'name': 'Renault Clio V', 'brand': 'Renault', 'model': 'Clio', 'year': 2018, 'price': 7500, 'is_new': 1,
         'other': 'Nothing'},
        {'name': 'Renault Clio IV', 'brand': 'Renault', 'model': 'Clio', 'year': 2015, 'price': 5000, 'is_new': 0,
         'other': 'Nothing'},
    ]

    josh_car = [
        {'name': 'My collection BMW', 'brand': 'BMW', 'model': 'A8', 'year': 2015, 'price': 75000, 'is_new': 0,
         'other': 'Nothing'},
        {'name': 'Ford focus 1.8', 'brand': 'Ford', 'model': 'Focus', 'year': 2012, 'price': 8000, 'is_new': 0,
         'other': 'Nothing'},
    ]

    users = {'oscar45': {'cars': oscar_car, 'username': 'oscar45', 'firstname': 'Oscar', 'lastname': 'Brown',
                       'email': 'Brown45@gmail.com', 'password': '123456'},
            'jane43': {'cars': jane_car, 'username': 'jane43', 'firstname': 'Jane', 'lastname': 'Berry',
                     'email': 'Jane43@gmail.com', 'password': '123456'},
            'josh67': {'cars': josh_car, 'username': 'josh67', 'firstname': 'Josh', 'lastname': 'Taylor',
                                'email': 'josh67@gmail.com', 'password': '123456'}}



# Start execution here!
if __name__ == '__main__':
    print('Starting buyacar population script...')
    populate()