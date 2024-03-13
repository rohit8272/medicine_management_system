from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view , authentication_classes ,permission_classes
from rest_framework.response import Response
from .serializer import Customer_serializer , Medicine_serializer
from .models import Customer 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from pymongo import MongoClient
from drf_yasg.utils import swagger_auto_schema

import os

# MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient("mongodb://localhost:27017")
db = client['medicines2']
collection = db['medicines_details2']

class Medicine_data(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
   
    @swagger_auto_schema(request_body=Medicine_serializer)
    def post(self , request):
        data = request.data
        serializer = Medicine_serializer(data = data)
        if not serializer.is_valid():
            return Response({"status" : 400 ,"errors": serializer.errors ,"message":"something went wrong"})
        serializer.save()
        collection.insert_one(serializer.data)
        return Response({"status" : 200 ,"data": serializer.data ,"message":"data add successfully ✔"})
        
    
    def get(self , request , uuid=None):
        if uuid == None:
            data = collection.find()
            serializer = Medicine_serializer(data , many=True)
            return Response({"status" : 200 ,"data": serializer.data})

        data = collection.find_one({"uuid" : uuid})
        serializer = Medicine_serializer(data)
        return Response({"status" : 200 ,"data": serializer.data})
    
    @swagger_auto_schema(request_body=Medicine_serializer)
    def put(self , request , uuid):
        old_data = collection.find_one({"uuid" : uuid})
        data = request.data
        serializer = Medicine_serializer(data = data)
        if not serializer.is_valid():
            return Response({"status" : 400 ,"errors": serializer.errors ,"message":"something went wrong"})
        new_data = {"$set" : serializer.data}
        collection.update_one(old_data , new_data)
        return Response({"status" : 200 ,"data": serializer.data ,"message":"data updated successfully ✔"})

    def delete(self , request , uuid):
        data = collection.find_one({"uuid" : uuid})
        serializer = Medicine_serializer(data)
        collection.delete_one({"uuid" : uuid})
        return Response({"status" : 200 ,"data": serializer.data ,"message":"data updated successfully ✔"})
   
class Customer_data(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(request_body=Customer_serializer)
    def post(self , request):
        data = request.data
        serializer = Customer_serializer(data = data)
        if not serializer.is_valid():
            return Response({"status" : 400 ,"errors": serializer.errors ,"message":"something went wrong"})
        serializer.save()
        return Response({"status" : 200 ,"data": serializer.data ,"message":"data add successfully ✔"})
        
    
    def get(self , request , uuid=None):
        if uuid == None:
            data = Customer.objects.all()
            serializer = Customer_serializer(data , many=True)
            return Response({"status" : 200 ,"data": serializer.data})

        data = Customer.objects.get(uuid = uuid)
        serializer = Customer_serializer(data)
        return Response({"status" : 200 ,"data": serializer.data})
    
    @swagger_auto_schema(request_body=Customer_serializer)
    def put(self , request , uuid):
        old_data = Customer.objects.get(uuid = uuid)
        data = request.data
        serializer = Customer_serializer(old_data , data = data)
        if not serializer.is_valid():
            return Response({"status" : 400 ,"errors": serializer.errors ,"message":"something went wrong"})
        serializer.save()
        return Response({"status" : 200 ,"data": serializer.data ,"message":"data updated successfully ✔"})

    def delete(self , request , uuid):
        data = Customer.objects.get(uuid = uuid)
        serializer = Customer_serializer(data)
        data.delete()
        return Response({"status" : 200 ,"data": serializer.data ,"message":"data updated successfully ✔"})
 