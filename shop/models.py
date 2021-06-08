from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    pub_date_created = models.DateTimeField(auto_now_add=True, null=True)
    phone_number = models.PositiveIntegerField( blank=True,null=True )

    def __str__(self):
        return self.first_name

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profiles(cls):
        profiles = cls.objects.all()
        return profiles

Towns = (
    ('Nairobi','Nairobi'),
    ('Kiambu','Kiambu'),
    ('Juja', 'Juja'),
    ('Thika', 'Thika'),
    ('Rongai','Rongai'),
    ('Nakuru','Nakuru'),
)
class Address(models.Model):
    user = models.OneToOneField(User,related_name='address',on_delete=models.CASCADE)
    city = models.CharField(max_length=20, choices=Towns, default='Nairobi')
    town = models.CharField(max_length=20,default='N/A')


    def __str__(self):
        return self.town

class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sell')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Item(models.Model):
    name = models.CharField(max_length = 300)
    image = models.ImageField(upload_to='neighimage/', null=True)
    description = models.CharField(max_length = 300)
    price = models.IntegerField(default='$ 0.0')
    category =  models.ForeignKey(Category, on_delete=models.CASCADE,related_name='categoryItem')
    posted_time = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(Seller, related_name='seller',on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-posted_time']

    def __str__(self):
        return self.name

    def save_item(self):
        self.save()

    def delete_item(self):
        self.delete()

    @classmethod
    def get_items(cls):
        items = cls.objects.all()
        return items

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='cartitems')
    item =  models.ForeignKey(Item, related_name='cartitem',on_delete=models.CASCADE, null=True)
    checkOutId = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.item.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='orderitem')
    item =  models.ForeignKey(Item, related_name='orderitem',on_delete=models.CASCADE, null=True)
    isSuccess = models.BooleanField(default=False)
    isPaidFor = models.BooleanField(default=False)
    checkOutId = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.item.name


class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sender')
    receive = models.ForeignKey(User, on_delete=models.CASCADE,related_name='receive')
    message = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)


class newsLetter(models.Model):
    email = models.EmailField(max_length=40)

    def __str__(self):
        return self.email


    def add(self,email):
        self.save(email)

    @classmethod
    def remove(self,emai):
        mail = cls.objects.get(email=emai)
        self.delete(mail)

class Transactions(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,
        related_name='transactions')
    phone = models.BigIntegerField(null=True)
    amount = models.BigIntegerField(null=True)
    MpesaReceipt = models.CharField(max_length=50,null=True)
    date = models.DateField(auto_now_add=True)
    checkoutRequestId = models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=100)
    direction = models.CharField(max_length=3)
    timestamp = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.MpesaReceipt