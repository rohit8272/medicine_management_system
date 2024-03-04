from rest_framework import serializers
from .models import Customer , Medicine
from django.contrib.auth.models import User

class User_srializer(serializers.ModelSerializer ):
    class Meta :
        model = User
        fields = ["username" , "password"]

    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'] )
        user.set_password(validated_data['password']) 
        user.save()
        return user

class Customer_serializer(serializers.ModelSerializer):
   
    class Meta:
        model = Customer
        fields = '__all__'



class Medicine_serializer(serializers.ModelSerializer):

    class Meta:
        model=Medicine
        fields='__all__'
        # fields = ['uuid', 'creted_at','name' , 'price' ,'expiry_date', 'weight_in_ML' ,'use_in_disease']
