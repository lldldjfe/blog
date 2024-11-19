from django.db import models

class User(models.Model):
    login = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.login

class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blogs')
    description = models.TextField()
    full_text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(auto_now=True)
    view = models.IntegerField(default=0)


class Comment(models.Model):
    comment = models.TextField()
    datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

class Like(models.Model):
    view = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, default=None)


class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    full_text = models.TextField()

    def __str__(self):
        return self.name


class Order(models.Model):
    summa = models.IntegerField()
    datetime_order = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
