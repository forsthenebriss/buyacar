from django.shortcuts import render, redirect
from django.http import HttpResponse
from rango.models import UserProfile, Car
from rango.forms import UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

#helper function for cookie testing
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
    
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
    '%Y-%m-%d %H:%M:%S')
    #if more than 1 day
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
            #update last visit
        request.session['last_visit'] = str(datetime.now())   
    else:    
        #set last visit
        request.session['last_visit'] = last_visit_cookie
    # Update/set the visits cookie
    request.session['visits'] = visits

#log out 
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

#restricted page only for logged in
@login_required
def restricted(request):
    context_dict = {}
    return render(request, 'rango/restricted.html', context=context_dict)

def user_login(request):
    if request.method == 'POST':
    #get the username and password provided by the user
        username = request.POST.get('username')
        password = request.POST.get('password')
        #check whether valid
        user = authenticate(username=username, password=password)
    
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                #inactive accounts cant log in
                return HttpResponse("Your Rango account is disabled.")
        else:
            #not possible for the user to login due to bad username/password
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    
    else:        
        return render(request, 'rango/login.html')   
            
            
def register(request):
    #initialized variable to false since nothing has beed done yet
    registered = False
    if request.method =='POST':
        #using the forms we grab information from data
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        #if both forms are valid, user is saved
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            #adding profile picture if one was given
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            if 'adress' in request.FILES:
                profile.picture = request.FILES['adress']
            if 'postcode' in request.FILES:
                profile.picture = request.FILES['postcode']
            profile.save()
            #change to true since the user has been registered
            registered = True
        #else prints errors
        else:
            print(user_form.errors, profile_form.errors)
    #else not a http form     
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    #finally render the request
    return render(request, 'rango/register.html',
                    context = {'user_form': user_form,
                                'profile_form': profile_form,
                                'registered': registered})


def show_seller(request, username):
    #creates a dict that can later be used to pass on stuff
    context_dict = {}
    try:
        #tries to get a seller and cars associated according to the slug
        seller = UserProfile.objects.get(slug=username)
        car = Car.objects.filter(seller=username)
        #adds findings to the dictionary
        new_cars = Car.objects.order_by('-year')[:5]
        cheap_cars = Car.objects.order_by('price')[:5] 
    
        context_dict['cars'] = car
        context_dict['sellers'] = seller
        context_dict['new'] = new_cars
        context_dict['cheap'] = cheap_cars
        
        #or throws an exeption
    except UserProfile.DoesNotExist:
        context_dict['sellers'] = None
        context_dict['pages'] = None
    #renders a response for the client with the dict required    
    return render(request, 'show_seller.html', context=context_dict)


def sellers(request):
    #creates a dict that can later be used to pass on stuff
    context_dict = {}
    try:
        #gets list of users for which is_seller is true
        seller_list = UserProfile.objects.filter(is_seller=True)
        #adds findings to the dictionary
        context_dict['sellers'] = seller_list
        
        new_cars = Car.objects.order_by('year')[:5]
        cheap_cars = Car.objects.order_by('price')[:5] 
        context_dict['new'] = new_cars
        context_dict['cheap'] = cheap_cars
        
        #or throws an exeption
    except UserProfile.DoesNotExist:
        context_dict['sellers'] = None
    #renders a response for the client with the dict required    
    return render(request, 'rango/sellers.html', context=context_dict)


#creates a view about
def about(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    context_dict['boldmessage'] = 'This tutorial has been put together by Romana Canigova'
    #renders a response for the client with the dict required
    return render(request, 'rango/about.html', context=context_dict)

#creates a view index
def index(request):
    #cookie function
    visitor_cookie_handler(request)
    #takes the 5 most liked categories as a list
    context_dict = {}
    #a dictionary to match the variables in templates
   
    #pcar_list = PCar.objects.order_by('-year')[:5]
    #ncar_list = NCar.objects.order_by('-price')[5:]
    category_list = {}
    page_list = {}
    #populating the dictionary 
    #context_dict['ncars'] = ncar_list
    #context_dict['pcar_list'] = pcar_list
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    #renders a response for the client with the dict required
    return render(request, 'rango/index.html', context=context_dict)


#creates a view index
def buying(request):
    #cookie function
    visitor_cookie_handler(request)
    #takes the 5 most liked categories as a list
    context_dict = {}
    #a dictionary to match the variables in templates
    category_list = {}
    page_list = {} 
    #populating the dictionary 
    
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    #renders a response for the client with the dict required
    return render(request, 'rango/buying.html', context=context_dict)



def enquire(request):
    return HttpResponse("Rango says hey there partner!")