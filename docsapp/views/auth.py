from docmanager.settings import CHANNELI_CLIENT_ID, CHANNELI_CLIENT_SECRET, REDIRECT_URI
from rest_framework.views import APIView
import requests
import json
from rest_framework.response import Response

class OAuthLogin(APIView):
    def get(self, request, *args, **kwargs):
        auth_code = request.query_params.get('code')
        client_id = CHANNELI_CLIENT_ID
        client_secret = CHANNELI_CLIENT_SECRET
        redirect_uri = REDIRECT_URI
        token_data = requests.post('https://channeli.in/open_auth/token/', data={
            'client_id' : client_id,
            'client_secret' : client_secret,
            'grant_type' : 'áuthorization_code',
            'redirect_uri' : redirect_uri,
            'code' : auth_code
        }).json()
        access_token = token_data['access_token']
        user_data = requests.get('https://channeli.in/open_auth/get_user_data/' , headers={
            'Authorization' : f"Bearer {access_token}"
        })
        return user_data.json()




