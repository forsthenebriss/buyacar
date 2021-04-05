import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'buyacar.settings')

import django

django.setup()
from rango.models import UserProfile, Car
from django.contrib.auth.models import User


def populate():
    oscar_car = [
        {'name': 'Nissan-pixo-88000km', 'brand': 'Nissan', 'model': 'Pixo', 'year': 2013, 'price': 3490, 'is_new': 0,
         'other': 'Nothing', 'picture': 'car_images/best_electric_cars_2021.jpg'}]

    jane_car = [
        {'name': 'Renault-Clio-V', 'brand': 'Renault', 'model': 'Clio', 'year': 2018, 'price': 7500, 'is_new': 1,
         'other': 'Nothing', 'picture': 'car_images/clioV.png'},
        {'name': 'Renault-Clio-IV', 'brand': 'Renault', 'model': 'Clio', 'year': 2015, 'price': 5000, 'is_new': 0,
         'other': 'Nothing', 'picture': 'car_images/clioIV.jpg'},
    ]

    josh_car = [
        {'name': 'My-collection-BMW', 'brand': 'BMW', 'model': 'A8', 'year': 2015, 'price': 75000, 'is_new': 0,
         'other': 'Nothing', 'picture': 'car_images/bmw-a8.jpg'},
        {'name': 'Ford-focus', 'brand': 'Ford', 'model': 'Focus', 'year': 2012, 'price': 8000, 'is_new': 0,
         'other': 'Nothing', 'picture': 'car_images/ford-focus.jpg'},
    ]

    users = {'oscar45': {'cars': oscar_car, 'username': 'oscar45', 'firstname': 'Oscar', 'lastname': 'Brown',
                         'email': 'Brown45@gmail.com', 'password': '123456', 'address': 'Glasgow',
                         'postcode': 'G1 1HA', 'picture': 'profile_images/oscar.png', 'is_seller':1},
             'jane43': {'cars': jane_car, 'username': 'jane43', 'firstname': 'Jane', 'lastname': 'Berry',
                        'email': 'Jane43@gmail.com', 'password': '123456', 'address': 'Glasgow',
                        'postcode': 'G1 1HA', 'picture': 'profile_images/jane.png', 'is_seller':1},
             'josh67': {'cars': josh_car, 'username': 'josh67', 'firstname': 'Josh', 'lastname': 'Taylor',
                        'email': 'josh67@gmail.com', 'password': '123456', 'address': 'Glasgow',
                        'postcode': 'G1 1HA', 'picture': 'profile_images/josh.png', 'is_seller':1}}

    for username, user_data in users.items():
        user = add_user(username, firstname=user_data['firstname'], lastname=user_data['lastname'],
                        email=user_data['email'], password=user_data['password'], address=user_data['address'],
                        postcode=user_data['postcode'], picture=user_data['picture'])
        for car in user_data['cars']:
            add_car(user, car['name'], car['brand'], car['model'], car['year'], car['price'], car['is_new'],
                    car['other'], car['picture'])

    # Print out the users we have added.
    for c in UserProfile.objects.all():
        for p in Car.objects.filter(seller=c):
            print(f'- {c}: {p}')


def add_car(user, name, brand, model, year, price, is_new, other, picture):
    car = Car.objects.get_or_create(seller=user, name=name)[0]
    car.name = name
    car.brand = brand
    car.model = model
    car.year = year
    car.price = price
    car.is_new = is_new
    car.other = other
    car.picture = picture
    car.save()
    return car


def add_user(username, firstname, lastname, email, password, address, postcode, picture):
    user = User.objects.get_or_create(username=username)[0]
    user.first_name = firstname
    user.last_name = lastname
    user.email = email
    user.set_password(password)
    user.save()

    profile = UserProfile.objects.get_or_create(user=user)[0]
    profile.user = user
    profile.user = user
    profile.website = ""
    profile.picture = picture
    profile.address = address
    profile.postcode = postcode
    profile.save()

    return profile


# Start execution here!
if __name__ == '__main__':
    print('Starting buyacar population script...')
    populate()
