from rest_framework import permissions, status
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from .serializers import *
from .permissions import IsModeratorAuthenticated
from .validation import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.backends import TokenBackend
from django.contrib.auth.models import User
from .models import UserProfile, UserRoles
from listings.views import get_property_details_json
import json
from django.views.decorators.csrf import csrf_exempt
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.linkedin_oauth2.views import LinkedInOAuth2Adapter

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.adapter import get_adapter
from .authenticate import SessionCsrfExemptAuthentication
from .authenticate import CsrfExempt


def json_status_response(status_code, message):
    to_json = {
    "message": message
    }
    response = HttpResponse(json.dumps(to_json))
    response.status_code = status_code
    return response 


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client

    def process_login(self):
        self.request.user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, self.user)
        access_token = get_tokens_for_user(self.request.user)['access']
        return Response({'token':access_token}, status=status.HTTP_200_OK)

import requests

class GoogleLogin(SocialLoginView):
    permission_classes = (permissions.AllowAny,)
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    # def post(self, request):
    #     resp = request.body
    #     body_unicode = resp.decode('utf-8')
    #     post_data = json.loads(body_unicode)
    #     payload = {'access_token': post_data["access_token"]}
    #     r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
    #     data = json.loads(r.text)

        
    def process_login(self):
        self.request.user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, self.user)

        access_token = get_tokens_for_user(self.request.user)['access']
        return Response({'token':access_token}, status=status.HTTP_200_OK)
    

class LinkedInSocialAuthView(SocialLoginView):
    permission_classes = (permissions.AllowAny,)
    adapter_class = LinkedInOAuth2Adapter
    client_class = OAuth2Client
    def process_login(self):
        self.request.user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, self.user)
        access_token = get_tokens_for_user(self.request.user)['access']
        
        return JsonResponse(
            {'status':status.HTTP_200_OK,
                'message':'success',
                'data':{
                    'token':access_token
                }
                })  


class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)

            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = (permissions.IsAuthenticated,)
    # def post(self, request, format=None):
        # request.user.auth_token.delete()
        # return Response(status=status.HTTP_200_OK)
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


def getUser(request):
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    print("token...", token)
    try:
        valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
    except:
        return {
            "status":400,
            "body":"Token is invalid or expired"
        }
    user_id = valid_data['user_id']
    if User.objects.filter(id = user_id).exists():
        return {"status":200, "body":User.objects.get(id = user_id)}
    else:
        return {
            "status":400,
            "body":"User not found"
        }
    


@csrf_exempt
def get_usertoken(request):
    print(request.user)
    if request.user.is_authenticated:
        print("authenticated..")
        access_token = get_tokens_for_user(request.user)['access']
        return JsonResponse({'token':access_token})
    return json_status_response(400, "Token not found")



class GetUserToken(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionCsrfExemptAuthentication,)
    
    def post(self, request):
        if request.user.is_authenticated:
            access_token = get_tokens_for_user(request.user)['access']
            return Response({'token':access_token}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

        

class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionCsrfExemptAuthentication,)
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user_data = serializer.check_user(data)
            if user_data['user']:
                login(request, user_data['user'])
                access_token = get_tokens_for_user(user_data['user'])['access']
                return Response({'token':access_token}, status=status.HTTP_200_OK)
            else:
                return Response({'message': user_data['message']}, status=401)
        return Response({'message': 'Invalid credentials'}, status=401)



def check_userrole(user_queryset, user):
    if UserRoles.objects.filter(user = user).exists():
        if user.role.is_moderator == True:
            role = "moderator"
    else:
        role = 'User'
    return role


def profile_json(request, user_queryset, profile_queryset, is_properties):
    role = check_userrole(user_queryset, user_queryset)
    properties_data = []
    jsonData = {
            'email':user_queryset.username,
            "fname":user_queryset.first_name,
            "lname":user_queryset.last_name,
            'email':user_queryset.email,
            'profile':f"{request.build_absolute_uri('/')[:-1]}/media/{str(profile_queryset.profile_picture)}",
            'id':user_queryset.id,
            'role':role,
            "company_logo":f"{request.build_absolute_uri('/')[:-1]}/media/{str(profile_queryset.company_logo)}",
            "company_name":profile_queryset.company_name,
            "mobile" :profile_queryset.mobile,
        }
    if is_properties and user_queryset.properties.exists():
        properties = [x.id for x in user_queryset.properties.all()]
        for property_id in properties:
            json_properties = get_property_details_json(property_id, request, is_profile= True)
            properties_data.append(json_properties[0])
        jsonData['properties']=properties_data
    return jsonData


# class GetUserProfile(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     authentication_classes = (JWTAuthentication, )
#     def post(self, request, format=None):
#         user = getUser(request)['body']
#         if UserProfile.objects.filter(user = user).exists():
#             profile = UserProfile.objects.get(user = user)
#             profile_data = profile_json(request, user, profile, is_properties=True)
#             return JsonResponse(profile_data)
#         else:
#             return Response({'error': 'Profile Not found'}, status=400)


class GerPublicProfile(CsrfExempt, APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []

    def post(self, request, format=None):
        body_unicode = request.body.decode('utf-8')
        post_data = json.loads(body_unicode)

        if User.objects.filter(id = post_data['user_id']).exists():
            user = User.objects.get(id = post_data['user_id'])
            profile = UserProfile.objects.get(user = user)
            profile_data = profile_json(request, user, profile, is_properties=True)
            return JsonResponse(profile_data)
        else:
            return Response({'error': 'Profile Not found'}, status=400)
        

@csrf_exempt
def get_userprofile(request):
    if getUser(request)['status'] == 200:
        print(getUser(request)['body'])
        user = getUser(request)['body']
        if UserProfile.objects.filter(user = user).exists():
            profile = UserProfile.objects.get(user = user)
            profile_data = profile_json(request, user, profile, is_properties=True)
            return JsonResponse(profile_data)
        else:
            return Response({'error': 'Profile Not found'}, status=400)
    else:
        return json_status_response(403, "Unauthorized")


from rest_framework import viewsets
class UpdateUserProfile(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


def convert_base_to_raw(user, img_data):
    format, imgstr = img_data.split(';base64,') 
    ext = format.split('/')[-1]     
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    file_name = f"{user.username}." + ext
    return {
        'file_name':file_name,
        'data':data
    }

@csrf_exempt
def update_userprofile(request):
    body_unicode = request.body.decode('utf-8')
    post_data = json.loads(body_unicode)
    user = getUser(request)['body']
    if UserProfile.objects.filter(user = user).exists():
        User.objects.filter(id = user.id).update(username = post_data['email'], email = post_data['email'],
                                                 first_name = post_data['fname'], last_name = post_data['lname']
                                                )
        company_name = post_data['company_name']
        UserProfile.objects.filter(user = user).update(
            company_name = company_name,
            mobile = post_data['mobile']
        )
        try:
            profile_Ins = UserProfile.objects.get(user = user)
            b_64_converted = convert_base_to_raw(user, post_data['profile'])
            profile_Ins.profile_picture.save(b_64_converted['file_name'],b_64_converted['data'],save=True)
            profile_Ins.save()
        except:
            pass

        try:
            profile_Ins = UserProfile.objects.get(user = user)
            b_64_converted = convert_base_to_raw(user, post_data['company_logo'])
            profile_Ins.company_logo.save(b_64_converted['file_name'],b_64_converted['data'],save=True)
            profile_Ins.save()
        except:
            pass
        return json_status_response(200, "Profile has been updated")
    else:
        return json_status_response(400, "Profile not found")
  