"""
Request:
--------
    {
        "name": "SRK",
        "username": "srkiiitn",
        "email": "gmail@srk.com",
        "password": "SRK123"
    }

Response:
---------

    {
        "result_msg": "Success"
    }
    
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


class Register_request_type(object):
    def __init__(self, name, username, password, email):
        self.name = name
        self.password = password
        self.email = email
        self.username = username


class Register_request_serializer(serializers.Serializer):
    
    name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()
    
    def create(self, validated_data):
        return Register_request_type(**validated_data)
    

class Register_response_type(object):
    def __init__(self, result_msg):
        self.result_msg = result_msg    

class Register_response_serializer(serializers.Serializer):
    
    result_msg = serializers.CharField()
    
    def create(self, validated_data):
        return Register_response_type(**validated_data)    

def create_new_user(name, username, email, password):
    
    try:
        user = User.objects.create_user(username = username
                                    , password = password
                                    , email = email
                                    , first_name = name)
    except:
        user = None
    
    return user
    

@api_view(['POST'])
def register(request):
    
    request_serializer = Register_request_serializer(data = request.data)

    if request_serializer.is_valid():
        request_object = request_serializer.save()
        
        name = request_object.name
        username = request_object.username
        password = request_object.password
        email = request_object.email
        
        registration_status = False
           
        if len(password) < 8:
            registration_status = False
        else:            
            user = None
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = create_new_user(name, username, email, password)
                if user is not None:
                    registration_status = True
            
        if registration_status == True:
            result_msg = "Welcome " + user.first_name + " !!!"
    
        else:
            result_msg = "Either username already exists or invalid password"
            
    else:
        result_msg = "Invalid Json Data"
        
    result_msg_type = Register_response_type(result_msg = result_msg)
    
    response_serializer = Register_response_serializer(result_msg_type)
    
    return Response(data = response_serializer.data
                    ,status = status.HTTP_200_OK)