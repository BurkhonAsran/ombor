from re import A
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from main.serializer import ClientSerializer, ProductSerializer
from .models import *
from rest_framework import permissions


class ClientDetail(APIView):
    permissions_classes = (permissions.IsAuthenticated)
    def get_object(self, pk):
        try:
            return Client.objects.get(id=pk)
        except:
            raise Http404
        
    def get(self, request, pk):
        snippet = self.get_object(pk)
        serializer = ClientSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk):
        client = self.get_object(pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = self.get_object(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ClientView(APIView):
    permissions_classes = (permissions.IsAuthenticated)
    def get(self, request):
        client = Client.objects.all()
        serializer = ClientSerializer(client, many=True)
        return Response(serializer.data)
  
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderView(APIView):
    permissions_classes = (permissions.IsAuthenticated)
    def get(self, request):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

