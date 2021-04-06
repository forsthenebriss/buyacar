from django import forms
from rango.models import UserProfile, Car
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    # additional properties
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
    

class UserProfileForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = UserProfile
        fields = ('website', 'picture', 'address', 'postcode', 'is_seller')


# class allowing to create a form from a preexisting model
class CarForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter name for your ad up to 128 characters")
    brand = forms.CharField(max_length=128, help_text="Please enter the manufacturer of your car")
    model = forms.CharField(max_length=128, help_text="Please enter car's model")
    year = forms.IntegerField()
    is_new = forms.BooleanField(required=False)
    price = forms.IntegerField()
    other = forms.CharField()
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    # helps provide association within model and model form
    class Meta:
        model = Car
        # excluding the category field from the form
        # better bcs we want to exclude less than include, otherwise specify
        exclude = ('seller', 'buyer')
       