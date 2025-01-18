from django.db import models
from django.core.validators import RegexValidator



# Methods
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

# Models
class WorkSample(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    url = models.URLField(max_length=255, null=True)
    image = models.ImageField(upload_to='worksample', null=True, blank=True)

    def __str__(self):
        return self.title 
    
    
from django.contrib.auth.models import User


class Client(models.Model):
    
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    
    # Extra Fields
    phone = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    image = models.ImageField(upload_to='accounts', null=True, blank=True)
    
    def __str__(self):
        return self.user.username
