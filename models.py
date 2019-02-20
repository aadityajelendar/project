from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()



class Product(models.Model):
    pid=models.IntegerField(primary_key=True)
    pname=models.CharField(max_length=20)
    pcost=models.DecimalField(max_digits=10,decimal_places=4)
    pmfdt=models.DateField()
    pexpdt=models.DateField()
    def __str__(self):
        return str(self.pid)
class Stock(models.Model):
    prodid = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    tot_qty=models.IntegerField()
    last_update=models.DateField()
    next_update=models.DateField()
class Cart(models.Model):
    username=models.CharField(max_length=20)
    pid=models.IntegerField()
    units=models.IntegerField()
    unitprice=models.DecimalField(max_digits=10,decimal_places=4)
    tuprice=models.DecimalField(max_digits=10,decimal_places=4)








