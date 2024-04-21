from typing import Iterable
from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    MinLengthValidator,
)
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

class Tag(models.Model):
    captions = models.CharField(max_length=20)

    def __str__(self) :
        return self.captions

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # auto check validated email address
    email = models.EmailField(null = True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name() 


class post(models.Model):
    # id column is created automatically
    # only change the struture of the model will trigger migration
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=150, blank=True)
    # image_name = models.CharField(max_length=150,blank=True)
    image = models.ImageField(upload_to="image", null= True)
    date = models.DateField(auto_now=True,null = True)

    # a pointer to Author entity
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    # only id field has automatically indexed, with other swtting index is quicker in searching
    slug = models.SlugField(unique=True, default="", blank=True, db_index=True)
    # textfield for long string
    content = models.TextField(validators=[MinLengthValidator(3)],blank = True)
    # no on_delted in manytomany
    tags = models.ManyToManyField(Tag)

    def get_absolute_url(self):
        return reverse("test_detail", args=[self.slug])

    def __str__(self):
        return f"{self.title}, author, {self.author}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    name = models.CharField(max_length = 50)
    email = models.EmailField()
    text = models.TextField(max_length = 300)
    date = models.DateField(auto_now=True,null = True)
    post = models.ForeignKey(post, on_delete = models.CASCADE, related_name = 'comments')















class Review(models.Model):
    username =models.CharField(max_length=100)
    review = models.TextField()
    rate = models.IntegerField()

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)


class Address(models.Model):
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)

    # in one to one use author to point that
    def __str__(self):
        return f"{self.city} {self.street}"
    

class Files(models.Model):
    image = models.ImageField(upload_to="iamge")
