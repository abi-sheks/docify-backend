from docmanager.settings import CHANNELI_CLIENT_ID, CHANNELI_CLIENT_SECRET, REDIRECT_URI, AUTH_URI
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
import requests
import json
from django import http
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User, AnonymousUser
from docsapp.serializers.authuser import AuthUserSerializer



#super simple view
class RegisterView(APIView):
    permission_classes = [AllowAny, ]
    authentication_classes = [TokenAuthentication, ]
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
    authentication_classes = [TokenAuthentication, ]
    def post(self, request, *args, **kwargs):
        user_srl = AuthUserSerializer(data=request.data)
        if user_srl.is_valid():
            user = None
            if not user:
                user = authenticate(username=user_srl.data['username'], password=user_srl.data['password'])
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'username' : user_srl.data['username'], 'email' : user_srl.data['email']}, status=status.HTTP_200_OK)
            else:
                return Response(data={'error' : 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'error' : 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# class OAuthRedirect(APIView):
#     permission_classes = []
#     authentication_classes=[]
#     def get(self, request, *args, **kwargs):
#         auth_code = request.query_params.get('code')
#         print(auth_code)
#         token_data = requests.post('https://channeli.in/open_auth/token/', data={
#             'client_id' : CHANNELI_CLIENT_ID,
#             'client_secret' : CHANNELI_CLIENT_SECRET,
#             'grant_type' : 'authorization_code',
#             'redirect_uri' : REDIRECT_URI,
#             'code' : auth_code
#         })
#         access_token = token_data['access_token']
#         user_data = requests.get('https://channeli.in/open_auth/get_user_data/' , headers={
#             'Authorization' : f"Bearer {access_token}"
#         })
#         print(user_data)
#         user, created = User.objects.get_or_create(
#             username=request.body.username,
#             email = request.body.email,
#         )
#         try: 
#             login(request, user)
#             return Response(data={"message" : "Auth successful"}, status=status.HTTP_200_OK)
#         except:
#             return Response(data={"error" : "Auth failed"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






