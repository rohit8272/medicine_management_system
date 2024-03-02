from django.shortcuts import render
from rest_framework.decorators import api_view , parser_classes
from rest_framework.response import Response
from .serializer import Customer_serializer , Medicine_serializer
from .db import conn
from .models import Customer , Medicine
from rest_framework.parsers import JSONParser

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
def get_medicine(request):
    # data = collection.find()
    data = Medicine.objects.all()
    serializer = Medicine_serializer(data  ,many= True)
    return Response({"data" : serializer.data})

@api_view(['GET'])
@parser_classes([JSONParser])
def get_medicine_by_id(request , uuid):
    data = collection.find_one({"uuid" : uuid})

    serializer = Medicine_serializer(data)
    # if not serializer.is_valid():
    #     return Response({"status" : 400 , "message" : serializer.errors})
    
    # instance = serializer.save()
    # response_data = serializer.data
    # response_data['uuid'] = instance.uuid
    print(serializer.data)
    return Response({"data" : serializer.data})

@api_view(['PUT'])
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
def delete_medicine(request , uuid):
    collection.delete_one({"uuid" : uuid})
    return Response("deleted")



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
def get_customer(request):
    query_set = Customer.objects.all()
    serializer = Customer_serializer(query_set , many=True)
    # context  = {"emp_details" : query_set}
    # print('query_set: ',query_set)
    # print('serialize_data: ' ,serializer.data)
    return Response({"data" : serializer.data})
