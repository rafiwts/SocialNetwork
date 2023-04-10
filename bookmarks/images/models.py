from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, # it always sets an automatic index for each object
                             related_name='images_created', 
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, 
                            blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d') # file
    description = models.TextField(blank=True) # an optional description
    created = models.DateField(auto_now_add=True, # with the date of creation/adding
                               db_index=True) # an automatic index for an iamge
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, # it creates an additional table --> id, image_id, user_id (frin settings)
                                        related_name='images_liked',
                                        blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) # a function which automatically generates a value to a 'slug' column if not given
            super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])