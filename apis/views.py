from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.models import Item,Profile
from django.contrib.auth.models import User
from .serializers import itemSerializer,profileSerializer,userSerializer
# Create your views here.

class ItemList(APIView):
    def get(self,request,format=None):
        all_items = Item.objects.all()
        serializedItems = itemSerializer(all_items,many=True)
        return Response(serializedItems.data)
    
    def post(self,request,format=None):
        serializers = itemSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.data,status=status.HTTP_400_BAD_REQUEST)

class profileList(APIView):
    def get(self,request,format=None):
        all_profiles = Profile.objects.all()
        serializedProfile = profileSerializer(all_profiles,many=True)
        return Response(serializedProfile.data)

class userList(APIView):
    def get(self,request,format=None):
        all_users = User.objects.all()
        serializedUsers = userSerializer(all_users,many=True)
        return Response(serializedUsers.data)
