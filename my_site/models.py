from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=30)


class Property(models.Model):
    TYPES = ((0, "flat"), (1, "house"))
    country = models.CharField(max_length=30)
    town = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    type = models.IntegerField(choices=TYPES)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)


class Client(models.Model):
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)


class Meeting(models.Model):
    property = models.ForeignKey(to=Property, on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    date = models.DateTimeField()

    class Meta:
        unique_together = (("property", "date"),)
