from django.db import models
from django.contrib.auth.models import User


# class User(models.Model):
#     user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.user.username


class Building(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=False)
    floor = models.IntegerField(null=False, default=1)
    area = models.FloatField(null=False, default=0)
    licence = models.CharField(max_length=10, null=False)
    image = models.ImageField(upload_to='course', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['area']


class Spent(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    category = models.CharField(max_length=255, blank=False, null=False)
    subject = models.CharField(max_length=255, blank=False, null=False)
    building = models.CharField(max_length=255, blank=False, null=False)
    date = models.CharField(max_length=5, blank=False, null=False)
    payer = models.CharField(max_length=255, blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)

    def __str__(self) -> str:
        return self.subject

    class Meta:
        ordering = ['id']

