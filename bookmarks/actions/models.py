from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
    user = models.ForeignKey('auth.User',
                             related_name='actions',
                             on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(ContentType, # it leads to a ContentType model
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)
    target_id = models.PositiveBigIntegerField(null=True, # the key for the object
                                               blank=True)
    target = GenericForeignKey('target_ct', 'target_id') # the key for the relation between a model and an object

    class Meta:
        ordering = ('-created',)


