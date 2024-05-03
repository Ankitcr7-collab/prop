from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers
import base64
from .models import UserProfile
from django.core.files.base import ContentFile
UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, clean_data):
        data = {}
        if UserModel.objects.filter(username=clean_data['email']).exists():
            return data['us']
        user_obj = UserModel.objects.create_user(username=clean_data['email'], password=clean_data['password'])
        user_obj.email = clean_data['email']
        user_obj.first_name = clean_data['first_name']
        user_obj.last_name = clean_data['last_name']
        user_obj.save()
        return user_obj
	

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('email', 'username')


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        data = {}
        user = authenticate(username=clean_data['email'], password=clean_data['password'])
        if not user is None:
            data['user'] = user
            return data 
        
        elif not UserModel.objects.filter(email=clean_data['email']).exists():
            data['message'] = f"The username was not found with the email {clean_data['email']}"
            data['user'] = None
            
        else:
            data['message'] = f"Invalid credentials"
            data['user'] = None
        
        return data
        
	
class ConsumptionDataSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ('car_mileage', 'gas_consumption', 'electricity_consumption', 'short_hauleflight_hours', \
			  'medium_hauleflight_hours', 'long_hauleflight_hours', 'bus_hours', 'train_mileage', 'timestamp', 'user')
    


class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.CharField(allow_blank=True, required=False)
    company_logo = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = UserProfile
        fields = ('id', 'profile_picture', 'company_logo', 'company_name', 'mobile')

    def create(self, validated_data):
        profile_picture_data = validated_data.pop('profile_picture', None)
        company_logo_data = validated_data.pop('company_logo', None)

        instance = UserProfile.objects.create(**validated_data)

        if profile_picture_data:
            instance.profile_picture = self.save_base64_image(profile_picture_data)
        if company_logo_data:
            instance.company_logo = self.save_base64_image(company_logo_data)
        
        instance.save()
        return instance

    def update(self, instance, validated_data):
        profile_picture_data = validated_data.pop('profile_picture', None)
        company_logo_data = validated_data.pop('company_logo', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if profile_picture_data:
            instance.profile_picture = self.save_base64_image(profile_picture_data)
        if company_logo_data:
            instance.company_logo = self.save_base64_image(company_logo_data)

        instance.save()
        return instance

    def save_base64_image(self, data):
        if data:
            format, imgstr = data.split(';base64,')  # splitting the base64 string
            ext = format.split('/')[-1]  # getting the extension
            data = ContentFile(base64.b64decode(imgstr), name=f'file.{ext}')  # decoding and creating the file
            return data
        return None
