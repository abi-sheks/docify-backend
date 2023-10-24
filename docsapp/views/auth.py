from docmanager.settings import CHANNELI_CLIENT_ID, CHANNELI_CLIENT_SECRET, REDIRECT_URI, AUTH_URI
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
import requests
import json
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User


class OAuthLogin(APIView):
    permission_classes = [AllowAny]
    authentication_Classes =[SessionAuthentication]
    def get(self, request, *args, **kwargs):
        channeli_uri = f"{AUTH_URI}?client_id={CHANNELI_CLIENT_ID}&redirect_uri={REDIRECT_URI}"
        return redirect(channeli_uri)

class OAuthRedirect(APIView):
    permission_classes = [AllowAny]
    authentication_classes=[SessionAuthentication]
    def get(self, request, *args, **kwargs):
        auth_code = request.query_params.get('code')
        token_data = requests.post('https://channeli.in/open_auth/token/', data={
            'client_id' : CHANNELI_CLIENT_ID,
            'client_secret' : CHANNELI_CLIENT_SECRET,
            'grant_type' : 'authorization_code',
            'redirect_uri' : REDIRECT_URI,
            'code' : auth_code
        })
        access_token = token_data['access_token']
        user_data = requests.get('https://channeli.in/open_auth/get_user_data/' , headers={
            'Authorization' : f"Bearer {access_token}"
        })
        print(user_data)
        user, created = User.objects.get_or_create(
            username=user_data['person']['full_name'],
            email = user_data['contact_information']['email_address'],
        )
        try: 
            login(request, user)
            return Response(data={"message" : "Auth successful"}, status=status.HTTP_200_OK)
        except:
            return Response(data={"error" : "Auth failed"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(data={"message" : "logged out successfully"}, status=status.HTTP_200_OK)





