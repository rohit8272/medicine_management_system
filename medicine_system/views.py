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
 














# @api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def add_medicine(request):
#     data = request.data
#     serializer = Medicine_serializer(data = data)

#     if not serializer.is_valid():
#         return Response({"status" : 400 , "message" : serializer.errors})
    
#     serializer.save()
#     collection.insert_one(serializer.data)
#     return Response({"data" : serializer.data})


# @api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def get_medicine(request):
#     data = collection.find()
#     serializer = Medicine_serializer(data  ,many= True)
#     return Response({"data" : serializer.data})


# @api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def get_medicine_by_id(request , uuid):
#     data = collection.find_one({"uuid" : uuid})
#     serializer = Medicine_serializer(data)
#     return Response({"data" : serializer.data})


# @api_view(['PUT'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def update_medicine(request , uuid):
#     old_data = collection.find_one({"uuid" : uuid})
#     data = request.data
#     serializer = Medicine_serializer(data = data)
#     if not serializer.is_valid():
#         return Response({"status" : 400 , "message" : serializer.errors})
#     new_data = {"$set" : serializer.data}
#     ## we can update without use of serializer
#     # new_data = {"$set" : data}
#     collection.update_one(old_data , new_data)
#     return Response({"data" : serializer.data})


# @api_view(['DELETE'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def delete_medicine(request , uuid):
#     data = collection.find_one({"uuid" : uuid})
#     serializer = Medicine_serializer(data)
#     collection.delete_one({"uuid" : uuid})
#     return Response({"data" : serializer.data})



# #### customers

# @api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def add_customer(request):
#     data = request.data
#     serializer = Customer_serializer(data = data)

#     if not serializer.is_valid():
#         return Response({"status" : 400 , "message" : serializer.errors})

#     serializer.save()
#     return Response({"data" : data})


# @api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def get_customer(request):
#     query_set = Customer.objects.all()
#     serializer = Customer_serializer(query_set , many=True)
#     return Response({"data" : serializer.data})


# @api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def get_customer_by_id(request ,uuid):
#     query_set = Customer.objects.get(uuid = uuid)
#     serializer = Customer_serializer(query_set)
#     return Response({"data" : serializer.data})


# @api_view(['PUT'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def update_customer(request , uuid):
#     data = request.data
#     query_set = Customer.objects.get(uuid = uuid)
#     serializer = Customer_serializer(query_set , data = data)
#     if not serializer.is_valid():
#         return Response({"status" : 400 , "message" : serializer.errors})

#     serializer.save()
#     return Response({"data" : serializer.data})


# @api_view(['DELETE'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def delete_customer(request ,uuid):
#     query_set = Customer.objects.get(uuid = uuid)
#     serializer = Customer_serializer(query_set)
#     query_set.delete()
#     return Response({"data" : serializer.data})
