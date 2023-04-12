from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class Profile(models.Model): # profile will be connected to a user
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, 
                                     null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d',
                              blank=True)
    
    def __str__(self):
        return f'{self.user.username} profile'


class Contact(models.Model):
    # the user who follows
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    # the user who is being followed
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


user_model = get_user_model()
user_model.add_to_class('following',     # dynamic addition of a column - We still use a User model
                        models.ManyToManyField('self',
                                               through=Contact,
                                               related_name='followers',
                                               symmetrical=False)) # follower does not have to be followed