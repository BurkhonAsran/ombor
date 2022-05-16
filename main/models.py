from http import client
from itertools import product
from tkinter import CASCADE
from unicodedata import category
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import AbstractBaseUser

class MyCustomerUser(AbstractBaseUser):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username =username, 
        )

        user.set_password(password)
        user.save(user=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            username =username, 
        )
        user.is_director = True
        user.is_seller = True
        user.is_keeper  = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    is_director = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_keeper = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyCustomerUser()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_director

    def has_module_perms(self, app_label):
        return True

class Client(models.Model):
    author = models.ForeignKey(AbstractBaseUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=244)
    address = models.CharField(max_length=255)
    debt = models.IntegerField(default=0)
    extra_phone = models.CharField(max_length=255,  null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    author = models.ForeignKey(AbstractBaseUser, on_delete=models.CASCADE)
    name = CharField(max_length=255)


class Product(models.Model):
    author = models.ForeignKey(AbstractBaseUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='Image/')
    size = models.CharField(max_length=255)
    quantity = models.IntegerField()

class Production(models.Model):
    author = models.ForeignKey(AbstractBaseUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    status = models.IntegerField(choices=(
        (1, 'created'),
        (2, 'accepted'),
        (3, 'rejected')

    ), default=1)


class Cash(models.Model):
    author = models.ForeignKey(AbstractBaseUser, on_delete=models.CASCADE)
    money = models.IntegerField()

class Payment(models.Model):
    author = models.ForeignKey(AbstractBaseUser, on_delete=models.CASCADE)
    money = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

class Order(models.Model):
    author = models.ForeignKey(AbstractBaseUser, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()

class OrderItem(models.Model):
    author = models.ForeignKey(AbstractBaseUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

