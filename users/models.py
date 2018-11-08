from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
COURSE_CHOICES = (
    ("COMPUTER SCIENCE", "Computer Science"),
    ("MARKETING", "Marketing"),
    ("HOSPITAILTY", "Hospitality"),
)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    course = models.CharField(max_length=30, default='Computer Science')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):#basically overriding the save method
        super().save()#just redoing the super class save method

        img = Image.open(self.image.path)#opens the image of the current instance

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)#overwrites the previous image
