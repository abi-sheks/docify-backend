from docmanager.settings import CHANNELI_CLIENT_ID, CHANNELI_CLIENT_SECRET, REDIRECT_URI, AUTH_URI
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
import requests
import json
from django import http
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User, AnonymousUser
from docsapp.serializers.authuser import AuthUserSerializer


def auth(username, email):
    try:
        user = User.objects.get(username=username)
        return user

    except User.DoesNotExist:
        User.objects.create(username=username, email=email)
        user = User.objects.get(username=username)
        return user
    
class WhoAmI(APIView):
    permission_classes=[AllowAny, ]
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(f"The user is {request.user}")
            return Response(data={"status" : "success", "username" : request.user.username, 'email' : request.user.email}, status=status.HTTP_200_OK)
        else:
            return Response(data={"status" : "error"}, status=status.HTTP_401_UNAUTHORIZED)
class RegisterView(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request, *args, **kwargs):
        user_serializer = AuthUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            username = user_serializer.data['username']
            email = user_serializer.data['email']
            return Response(data={'username' : username, 'email' : email}, status=status.HTTP_200_OK)
        else:
            return Response(data={'error' : 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(APIView):
    permission_classes = [AllowAny, ]
    def get(self, request, *args, **kwargs):
        channeli_uri = f"{AUTH_URI}?client_id={CHANNELI_CLIENT_ID}&redirect_uri={REDIRECT_URI}"
        return redirect(channeli_uri)
    # def post(self, request, *args, **kwargs):
    #     user_srl = AuthUserSerializer(data=request.data)
    #     if user_srl.is_valid():
    #         user = None
    #         if not user:
    #             user = authenticate(username=user_srl.data['username'], password=user_srl.data['password'])
    #         if user:
    #             token, _ = Token.objects.get_or_create(user=user)
    #             return Response({'token': token.key, 'username' : user_srl.data['username'], 'email' : user_srl.data['email']}, status=status.HTTP_200_OK)
    #         else:
    #             return Response(data={'error' : 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response(data={'error' : 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class OAuthRedirect(APIView):
    permission_classes = [AllowAny, ]
    def get(self, request, *args, **kwargs):
        auth_code = request.query_params.get('code')
        token_data = requests.post('https://channeli.in/open_auth/token/', data={
            'client_id' : CHANNELI_CLIENT_ID,
            'client_secret' : CHANNELI_CLIENT_SECRET,
            'grant_type' : 'authorization_code',
            'redirect_uri' : REDIRECT_URI,
            'code' : auth_code
        }).json()
        access_token = token_data['access_token']
        user_data = requests.get('https://channeli.in/open_auth/get_user_data/' , headers={
            'Authorization' : f"Bearer {access_token}"
        }).json()
        print(user_data)
        email = user_data['contactInformation']['emailAddress']
        for role in user_data['person']['roles']:
            if (role['role'] == "Maintainer"):
                is_member = True
        if is_member:
            try:
                user = auth(username=user_data['username'], email=email)
            except:
                return Response(data={"error" : "unable to create user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # token, _ = Token.objects.get_or_create(user=user)
            try: 
                login(request, user)
                return redirect("http://localhost:3000/home")
            except:
                return Response(data={"error" : "Auth failed"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={"error" : "Not a member"})
        

class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






