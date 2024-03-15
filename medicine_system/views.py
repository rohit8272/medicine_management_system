from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import Customer_serializer , Medicine_serializer
from .models import Customer 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from pymongo import MongoClient
from drf_yasg.utils import swagger_auto_schema
from django.http import JsonResponse
import json
from bson import json_util , ObjectId
import os

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client["medicines2"]
collection = db["medicines_details2"]

class Medicine_data(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
   
    @swagger_auto_schema(request_body=Medicine_serializer)
    def post(self , request):
        data = request.data  
        serializer = Medicine_serializer(data = data)      
        if not serializer.is_valid():  
            return Response({"errors": serializer.errors ,"message":"something went wrong" }, status=status.HTTP_400_BAD_REQUEST)

        collection.insert_one(data)
        return Response({"message":"data add successfully ✔"}, status=status.HTTP_201_CREATED )       
    
    def get(self , request , _id=None):
        if _id == None:
            data = collection.find()
            json_data =  json.loads(json_util.dumps(data))
            return JsonResponse(json_data , safe=False , status=status.HTTP_200_OK)
        
        id = ObjectId(_id)
        data = collection.find_one({"_id" : id})
        json_data =  json.loads(json_util.dumps(data))
        if not json_data:
            return Response({"message":f"the data is not available for given id: {id}" }, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(json_data , safe=False , status=status.HTTP_200_OK)

    
    @swagger_auto_schema(request_body=Medicine_serializer)
    def put(self , request , _id):
        id = ObjectId(_id)
        old_data = collection.find_one({"_id" : id})
        data = request.data
        serializer = Medicine_serializer(data = data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors ,"message":"something went wrong"} , status=status.HTTP_400_BAD_REQUEST)
        new_data = {"$set" : serializer.data}
        collection.update_one(old_data , new_data)
        return Response({"data": serializer.data ,"message":"data updated successfully ✔"}, status=status.HTTP_200_OK)

    def delete(self , request , _id):
        id = ObjectId(_id)
        data = collection.find_one({"_id" : id})
        if not data:
            content = {"message" : f"data does not exist for this given ID: {id}"}
            return Response(content , status=status.HTTP_404_NOT_FOUND )
        collection.delete_one({"_id" : id})
        return Response({"message" : "data deleted successfully"} , status=status.HTTP_200_OK)
   
class Customer_data(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(request_body=Customer_serializer)
    def post(self , request):
        data = request.data
        serializer = Customer_serializer(data = data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors ,"message":"something went wrong" }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"data": serializer.data ,"message":"data add successfully ✔"} , status=status.HTTP_201_CREATED)
        
    
    def get(self , request , uuid=None):
      try:
        if uuid == None:
            data = Customer.objects.all()
            serializer = Customer_serializer(data , many=True)
            return Response({"data": serializer.data} , status=status.HTTP_200_OK)
        data = Customer.objects.get(uuid = uuid)
        serializer = Customer_serializer(data)
        return Response({"data": serializer.data},status=status.HTTP_200_OK)
    
      except Customer.DoesNotExist:
        content = {"message" : f"data is not available for this given ID: {uuid}"}
        return Response(content , status=status.HTTP_404_NOT_FOUND )

    
    @swagger_auto_schema(request_body=Customer_serializer)
    def put(self , request , uuid):
        old_data = Customer.objects.get(uuid = uuid)
        data = request.data
        serializer = Customer_serializer(old_data , data = data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors ,"message":"something went wrong"} , status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"data": serializer.data ,"message":"data updated successfully ✔"}, status=status.HTTP_200_OK)

    def delete(self , request , uuid):
      try:
        data = Customer.objects.get(uuid = uuid)
        data.delete()
        return Response({"message":"data deleted successfully ✔"} , status=status.HTTP_200_OK)
      except Customer.DoesNotExist:
        content = {"message" : f"data is not available for this given ID: {uuid}"}
        return Response(content , status=status.HTTP_404_NOT_FOUND )
          