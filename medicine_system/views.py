from django.shortcuts import render
from rest_framework.decorators import api_view , authentication_classes ,permission_classes
from rest_framework.response import Response
from .serializer import Customer_serializer , Medicine_serializer
from .db import conn
from .models import Customer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

db = conn['medicines']
collection = db['medicines_details']

@api_view(['POST'])
def add_medicine(request):
    data = request.data
    serializer = Medicine_serializer(data = data)

    if not serializer.is_valid():
        return Response({"status" : 400 , "message" : serializer.errors})
    
    serializer.save()
    collection.insert_one(serializer.data)
    return Response({"data" : serializer.data})


@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def get_medicine(request):
    data = collection.find()
    serializer = Medicine_serializer(data  ,many= True)
    return Response({"data" : serializer.data})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_medicine_by_id(request , uuid):
    data = collection.find_one({"uuid" : uuid})
    serializer = Medicine_serializer(data)
    return Response({"data" : serializer.data})


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_medicine(request , uuid):
    old_data = collection.find_one({"uuid" : uuid})
    data = request.data
    serializer = Medicine_serializer(data = data)
    if not serializer.is_valid():
        return Response({"status" : 400 , "message" : serializer.errors})
    new_data = {"$set" : serializer.data}
    ## we can update without use of serializer
    #  new_data = {"$set" : data}
    collection.update_one(old_data , new_data)
    return Response({"data" : serializer.data})


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_medicine(request , uuid):
    data = collection.find_one({"uuid" : uuid})
    serializer = Medicine_serializer(data)
    collection.delete_one({"uuid" : uuid})
    return Response({"data" : serializer.data})



#### customers

@api_view(['POST'])
def add_customer(request):
    data = request.data
    serializer = Customer_serializer(data = data)

    if not serializer.is_valid():
        return Response({"status" : 400 , "message" : serializer.errors})

    serializer.save()
    return Response({"data" : data})


@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def get_customer(request):
    query_set = Customer.objects.all()
    serializer = Customer_serializer(query_set , many=True)
    return Response({"data" : serializer.data})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_customer_by_id(request ,uuid):
    query_set = Customer.objects.get(uuid = uuid)
    serializer = Customer_serializer(query_set)
    return Response({"data" : serializer.data})


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_customer(request ,uuid):
    data = request.data
    query_set = Customer.objects.get(uuid = uuid)
    serializer = Customer_serializer(query_set , data = data)
    if not serializer.is_valid():
        return Response({"status" : 400 , "message" : serializer.errors})

    serializer.save()
    return Response({"data" : serializer.data})


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_customer(request ,uuid):
    query_set = Customer.objects.get(uuid = uuid)
    serializer = Customer_serializer(query_set)
    query_set.delete()
    return Response({"data" : serializer.data})
