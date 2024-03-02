from rest_framework import serializers
from .models import Customer , Medicine

class Customer_serializer(serializers.ModelSerializer):
   
    class Meta:
        model = Customer
        fields = '__all__'



class Medicine_serializer(serializers.ModelSerializer):

    class Meta:
        model=Medicine
        fields='__all__'
        # fields = ['uuid', 'creted_at','name' , 'price' ,'expiry_date', 'weight_in_ML' ,'use_in_disease']
