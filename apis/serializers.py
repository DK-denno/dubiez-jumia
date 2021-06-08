from rest_framework import serializers
from shop.models import Item,Profile
from django.contrib.auth.models import User

class profileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user','pub_date_created','phone_number']

class itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name','image','description','price','category','posted_time','seller']

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']
        
