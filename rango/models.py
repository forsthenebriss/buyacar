from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class UserProfile(models.Model):
    #creates user and links him to user model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #additional requirements
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    adress = models.CharField(max_length=300)
    postcode = models.CharField(max_length=6)
    is_seller = models.BooleanField(default=False)
    #string for better handling
    slug = models.SlugField(unique=True, null=True)
    
    #each time category is updated, the slug is updated as well
    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username


        
class Car(models.Model):
    #if deleted, everything connected deleted with the category
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    #a title string of maximum 128 chars
    name = models.CharField(max_length=128)
    brand = models.CharField(max_length=128)
    model = models.CharField(max_length=128)
    year = models.IntegerField(default=2021)
    price = models.IntegerField(default=0)
    is_new = models.BooleanField(default=True)
    other = models.TextField()
    picture = models.ImageField(upload_to='car_images', blank=True)
    #return name as string for easier manipulation
    def __str__(self):
        return self.name