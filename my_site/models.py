from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    USERNAME_FIELD = "username"
    email = models.CharField(max_length=60, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = BaseUserManager()

    def get_full_name(self):
        return self.username + " " + self.email

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Client(models.Model):
    user = models.OneToOneField(User)
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)


class Owner(models.Model):
    user = models.OneToOneField(User)


class Property(models.Model):
    TYPES = ((0, "flat"), (1, "house"))
    country = models.CharField(max_length=30)
    town = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    type = models.IntegerField(choices=TYPES)
    user = models.ForeignKey(to=Owner, on_delete=models.CASCADE)


class Meeting(models.Model):
    property = models.ForeignKey(to=Property, on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    date = models.DateTimeField()

    class Meta:
        unique_together = (("property", "date"),)

# class UserProfile(models.Model):
#     # This line is required. Links UserProfile to a User model instance.
#     user = models.OneToOneField(U)
#
#     # The additional attributes we wish to include.
#     website = models.URLField(blank=True)
#
#     # picture = models.ImageField(upload_to='profile_images', blank=True)
#
#     # Override the __unicode__() method to return out something meaningful!
#     def __unicode__(self):
#         return self.user.username
