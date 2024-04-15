from django.contrib.auth.models import User, AbstractUser
from django.db import models

from django.conf import settings


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Institution(models.Model):
    TYPE_CHOICES = [
        ('fundacja', 'Fundacja'),
        ('organizacja_pozarządowa', 'Organizacja pozarządowa'),
        ('zbiórka_lokalna', 'Zbiórka lokalna')
    ]

    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.CharField(choices=TYPE_CHOICES, default='fundacja', max_length=32)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name




class Donation(models.Model):
    quantity = models.IntegerField()
    category = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone = models.CharField(max_length=18)
    city = models.CharField(max_length=64)
    zipcode = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None)


