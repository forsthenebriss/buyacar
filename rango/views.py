from django.shortcuts import render, redirect
from django.http import HttpResponse
from rango.models import UserProfile, Car
from rango.forms import UserForm, UserProfileForm, CarForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


# helper function for cookie testing
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    # if more than 1 day
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # update last visit
        request.session['last_visit'] = str(datetime.now())
    else:
        # set last visit
        request.session['last_visit'] = last_visit_cookie
    # Update/set the visits cookie
    request.session['visits'] = visits


# log out
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

#search with filter option
def search(request):
    context_dict = {}
    if request.method == 'POST':
        text = request.POST.get('search_box')
        new = False
        if request.POST.get('new_car') is not None:
            new = request.POST.get('new_car')
        print(text)

        result = Car.objects.filter(name__icontains=text, is_new=new)
        context_dict['search_result'] = result

    try:
        # gets list of users for which is_seller is true
        seller_list = UserProfile.objects.filter(is_seller=True)
        # adds findings to the dictionary
        context_dict['sellers'] = seller_list
        #adds lists of new and cheap cars into the dictionary
        new_cars = Car.objects.filter(is_new=True).order_by('year').reverse()[:5]
        cheap_cars = Car.objects.order_by('price')[:5]
        context_dict['new'] = new_cars
        context_dict['cheap'] = cheap_cars

        # or throws an exeption
    except UserProfile.DoesNotExist:
        context_dict['sellers'] = None
    return render(request, 'rango/search.html', context=context_dict)


def user_login(request):
    if request.method == 'POST':
        # get the username and password provided by the user
        username = request.POST.get('username')
        password = request.POST.get('password')
        # check whether valid
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                # inactive accounts cant log in
                return HttpResponse("Your Rango account is disabled.")
        else:
            # not possible for the user to login due to bad username/password
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'rango/login.html')


def register(request):
    # initialized variable to false since nothing has beed done yet
    registered = False
    if request.method == 'POST':
        # using the forms we grab information from data
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # if both forms are valid, user is saved
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # adding profile picture if one was given
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            if 'address' in request.FILES:
                profile.picture = request.FILES['address']
            if 'postcode' in request.FILES:
                profile.picture = request.FILES['postcode']
            profile.save()
            # change to true since the user has been registered
            registered = True
        # else prints errors
        else:
            print(user_form.errors, profile_form.errors)
    # else not a http form
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # finally render the request
    return render(request, 'registration/registration_form.html',
                  context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


@login_required
def add_car(request, username):
    # initialized variable to false since nothing has beed done yet
    try:
        seller = UserProfile.objects.get(slug=username)

    except UserProfile.DoesNotExist:
        seller = None
    # car needs to have a seller
    if seller is None:
        return redirect('/rango/')

    form = CarForm()

    if request.method == 'POST':
        # using the forms we grab information from data
        form = CarForm(request.POST)

        # if both forms are valid, user is saved
        if form.is_valid():
            if seller:
                car = form.save(commit=False)
            car.seller = seller
            seller.is_seller = True
            if 'picture' in request.FILES:
                car.picture = request.FILES['picture']

            car.save()
            # adding profile picture if one was given
            return redirect(reverse('rango:sellers'))
        # else prints errors
        else:
            print(form.errors)
    context_dict = {'form': form, 'seller': seller}
    return render(request, 'rango/add_car.html', context=context_dict)


def show_seller(request, username):
    # creates a dict that can later be used to pass on stuff
    context_dict = {}
    try:
        # gets list of users for which is_seller is true
        seller = UserProfile.objects.get(slug=username)
        cars = Car.objects.filter(seller=seller)
        # adds findings to the dictionary
        context_dict['sellers'] = seller
        context_dict['cars'] = cars
        #adds lists of new and cheap cars into the dictionary
        new_cars = Car.objects.filter(is_new=True).order_by('year').reverse()[:5]
        cheap_cars = Car.objects.order_by('price')[:5]
        context_dict['new'] = new_cars
        context_dict['cheap'] = cheap_cars
    # or throws an exeption
    except UserProfile.DoesNotExist:
        context_dict['sellers'] = None
    # renders a response for the client with the dict required
    return render(request, 'rango/show_seller.html', context=context_dict)


def sellers(request):
    # creates a dict that can later be used to pass on stuff
    context_dict = {}
    try:
        # gets list of users for which is_seller is true
        seller_list = UserProfile.objects.filter(is_seller=True)
        # adds findings to the dictionary
        context_dict['sellers'] = seller_list
        #adds lists of new and cheap cars into the dictionary
        new_cars = Car.objects.filter(is_new=True).order_by('year').reverse()[:5]
        cheap_cars = Car.objects.order_by('price')[:5]
        context_dict['new'] = new_cars
        context_dict['cheap'] = cheap_cars

        # or throws an exeption
    except UserProfile.DoesNotExist:
        context_dict['sellers'] = None
    # renders a response for the client with the dict required
    return render(request, 'rango/sellers.html', context=context_dict)

# creates a view index
def index(request):
    # cookie function
    visitor_cookie_handler(request)
    #adds lists of new and cheap cars into the dictionary
    context_dict = {}
    new_cars = Car.objects.filter(is_new=True).order_by('year').reverse()[:5]
    cheap_cars = Car.objects.order_by('price')[:5]
    context_dict['new'] = new_cars
    context_dict['cheap'] = cheap_cars
    return render(request, 'rango/index.html', context=context_dict)


# creates a view index
def buying(request, name):
    # cookie function
    context_dict = {}
    visitor_cookie_handler(request)
    #gets the requested car
    car = Car.objects.get(name=name)
    context_dict['car'] = car
    # renders a response for the client with the dict required
    return render(request, 'rango/buying.html', context=context_dict)


def enquire(request):
    return HttpResponse("Rango says hey there partner!")
