from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import *
from accounts.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from django.core.files.base import ContentFile

# from rest_framework import permissions, status
# from rest_framework.authtoken.models import Token
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from accounts import views as accounts_views

from django.core.paginator import EmptyPage, Paginator
import math

def get_all_features(request):
    features = [x.name for x in FeatureMaster.objects.all()]
    return JsonResponse(features, safe=False)

def json_status_response(status_code, message):
    to_json = {
    "message": message
    }
    response = HttpResponse(json.dumps(to_json))
    response.status_code = status_code
    return response 

def get_features_json(property):
    features = []
    if property.feature:
        features = list(property.feature.all().values_list('name'))
    return features

def get_types_json(property):
    types = ''
    if property.type.exists():
        types = property.type.all()[0].name
    return types

def get_property_json(query_set, request):
    # Check for user
    datas_list = []
    for property in query_set:
        user = property.user
        profile = UserProfile.objects.get(user = user)
        profile_data = accounts_views.profile_json(request, user, profile, is_properties=False)
        features = get_features_json(property)  
        types = get_types_json(property)  
        images = get_all_property_images(property, request)
        if property.expire_date:
            days_until_expiration = (property.expire_date - timezone.now()).days
        else:
            days_until_expiration = None
	
        datas_list.append(
        {
        'id':property.id,
        'title':property.title,
        'type':types,
        'price':property.price,
        'adddress':property.adddress,
        'city':property.city,
        'postal_code':property.postal_code,
        'county':property.county,
        'state':property.state,
        'lat':property.lat,
        'lon':property.lon,

        'content':property.content,
        'area_unit':property.area_unit,
        'buildup_area_unit':property.buildup_area_unit,
        'buildup_area':property.buildup_area,
        'carpet_area':property.carpet_area,
        'carpet_area_unit':property.carpet_area_unit,
        'bathroom':property.bathroom,
        'bedroom':property.bedroom,

        'video_link':property.video_link,

        'pub_date':property.pub_date,
	"days_until_expiration":days_until_expiration,
        'main_image':f"{request.build_absolute_uri('/')[:-1]}/media/{str(property.main_image)}",
        'profile_data':profile_data,
        "features":features,
        "all_images":images,

        })
    return datas_list

def listing_pagination(request,properties, post_data):
    resp_data = []
    PRODUCTS_PER_PAGE = 20
    page = post_data['page_no']
    product_paginator = Paginator(properties, PRODUCTS_PER_PAGE)
    try:
        properties = product_paginator.page(page)
    except EmptyPage:
        properties = product_paginator.page(product_paginator.num_pages)
    except:
        properties = product_paginator.page(PRODUCTS_PER_PAGE)

    json_properties = get_property_json(properties, request)

    page_ob = {'start':product_paginator.page_range.start,
               'end':product_paginator.page_range.stop,
               'current_idx':page}
    
    resp_data.append({'page_obj':page_ob})
    resp_data.append({'properties':json_properties})
    return resp_data

from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .authenticate import SessionCsrfExemptAuthentication


@csrf_exempt
def get_all_listings(request):
    body_unicode = request.body.decode('utf-8')
    post_data = json.loads(body_unicode)
    properties = Properties.objects.all().order_by('-pub_date')
    resp_data = listing_pagination(request, properties, post_data)
    return JsonResponse(resp_data, safe=False)

# Property details json
def get_all_property_images(property, request):
        images_lst = []
        images_list = property.images.all()
        for image in images_list:
            img_path = f"{request.build_absolute_uri('/')[:-1]}/media/{str(image.images)}"
            images_lst.append(img_path)
        return images_lst  


def get_property_details_json(property_id, request, is_profile):    
    property = Properties.objects.get(id = property_id)
    datas_list = []
    features = get_features_json(property)  
    types = get_types_json(property)  
    images = get_all_property_images(property, request)

    # Check for user
    user = property.user
    profile = UserProfile.objects.get(user = user)
    profile_data = accounts_views.profile_json(request, user, profile, is_properties=False)
    if property.expire_date:
         days_until_expiration = (property.expire_date - timezone.now()).days
    else:
         days_until_expiration = None
    datas_list.append(
    {
        'id':property.id,
        'status':property.status,
        'is_ready_to_publish':property.is_ready_to_publish,
        'title':property.title,
        'type':types,
	'area_unit':property.area_unit,
        'buildup_area_unit':property.buildup_area_unit,
        'buildup_area':property.buildup_area,
        'carpet_area':property.carpet_area,
        'carpet_area_unit':property.carpet_area_unit,
        'bathroom':property.bathroom,
        'bedroom':property.bedroom,
        'price':property.price,
        'adddress':property.adddress,
        'city':property.city,
        'county':property.county,
        'postal_code':property.postal_code,
        "lat":property.lat,
        "lon":property.lon,
        'content':property.content,
        'pub_date':property.pub_date,
	"days_until_expiration":days_until_expiration,
        'main_image':f"{request.build_absolute_uri('/')[:-1]}/media/{str(property.main_image)}",
        'video_link':property.video_link,
        'images':images,
        'features':features,
        'user_profile':profile_data      
        })
    return datas_list

@csrf_exempt
def get_property_details(request):
    body_unicode = request.body.decode('utf-8')
    post_data = json.loads(body_unicode)
    property_id = post_data['property_id']
    if not Properties.objects.filter(id = property_id).exists():
        return json_status_response(400, 'Property Not Found')
    
    property_id = post_data['property_id']
    json_properties = get_property_details_json(property_id, request, is_profile=True)
    return JsonResponse(json_properties, safe=False)


@csrf_exempt
def property_search(request):
    body_unicode = request.body.decode('utf-8')
    query = json.loads(body_unicode)
    properties = Properties.objects.all()
    if len(query['county']) != 0:
        properties = properties.filter(
            county__in = query['county']
        )

    if len(query['features']) != 0:
        properties = properties.filter(
            feature__name__in = query['features']
        )

    if len(query['property_type']) != 0:
        properties = properties.filter(
            type__name__in = query['property_type']
        )
        
    if len(query['cities']) != 0:
        properties = properties.filter(
            city__in = query['cities']
        )
    
    properties = properties.filter( price__gte = query['priceFrom'],
        price__lte = query['priceTo'],
    )
    resp_data = listing_pagination(request,properties, query)    
    return JsonResponse(resp_data, safe=False)


def ordering_properties(query, properties):
    if query:
        if query['sort_type'] == "price":
            if query['sort_order'] == 'ascending':
                properties = properties.order_by('price')

            if query['sort_order'] == 'descending':
                properties = properties.order_by('-price')

        if query['sort_type'] == "date":
            if query['sort_order'] == "ascending":
                properties = properties.order_by('pub_date')
                
            if query['sort_order'] == "descending":
                properties = properties.order_by('-pub_date')
    
    return properties

@csrf_exempt
def order_listings(request):
    body_unicode = request.body.decode('utf-8')
    query = json.loads(body_unicode)
    property_ids = query['property_ids']
    properties = Properties.objects.filter(id__in = property_ids)
    json_properties = ordering_properties(query, properties)
    resp_data = listing_pagination(request,json_properties, query)   
    return JsonResponse(resp_data, safe=False)

# convert image to base65
def convert_base_to_raw(img_data):
    format, imgstr = img_data.split(';base64,') 
    ext = format.split('/')[-1]     
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    file_name = "event." + ext
    return {
        'file_name':file_name,
        'data':data
    }

def update_property_images(property, all_images):
    for idx, image in enumerate(all_images):
        try:
            img_ob = PropertyImage(
                property = property
            )
            b_64_converted = convert_base_to_raw(image)
            file_name = f"{property.title}_{idx}.jpg"
            img_ob.images.save(file_name, b_64_converted['data'],save=True)
            img_ob.save()
        except:
            pass    


def update_property_features(property, features):
    features_ob = property.feature.all()
    for feature in features_ob:
        if feature.name not in features:
            property.feature.remove(feature)
    new_features = FeatureMaster.objects.filter(name__in = features)
    property.feature.add(*new_features)


def update_property_types(property, type):
    if property.type.exists():
        for prop in property.type.all():
            if prop.name == type:
                pass
            else:
                property.type.remove(prop.id)
                new_types = TypeMaster.objects.filter(name = type)
                property.type.add(*new_types)

@csrf_exempt
def add_property(request):
    body_unicode = request.body.decode('utf-8')
    post_data = json.loads(body_unicode)
    user = accounts_views.getUser(request)['body']
    new_property = Properties(
        user = user,
        title = post_data['title'],
        price = post_data['price'],
        adddress = post_data['adddress'],
        county = post_data['county'],
        state = post_data['state'],
        city = post_data['city'],
        postal_code = post_data['postal_code'],
        content = post_data['content'],
        
        # dimensions
        area_unit = post_data['area_unit'],
        buildup_area_unit = post_data['buildup_area_unit'],
        buildup_area = post_data['buildup_area'],
        carpet_area = post_data['carpet_area'],
        carpet_area_unit = post_data['carpet_area_unit'],
        bathroom= post_data['bathroom'],
        bedroom= post_data['bedroom']
    )
    new_property.save()
    if TypeMaster.objects.filter(name = post_data['type']).exists():
        new_property.type.add(TypeMaster.objects.get(name = post_data['type']))
    new_property.save()

    if len(post_data['video_link'])>1:
        new_property.video_link = post_data['video_link']

    # save images
    # main image
    try:
        b_64_converted = convert_base_to_raw(post_data['main_image'])
        new_property.main_image.save(b_64_converted['file_name'],
                                     b_64_converted['data'],save=True)
        # new_property.save()
    except:
        pass

    # all images
    if len(post_data['all_images']) >= 1:
        update_property_images(new_property, post_data['all_images'])

    # features
    if len(post_data['features']) >= 1:
        update_property_features(new_property, post_data['features'])
    return JsonResponse({"message":'success'})

@csrf_exempt
def update_property(request):
    body_unicode = request.body.decode('utf-8')
    post_data = json.loads(body_unicode)
    # Property ob
    if Properties.objects.filter(id = post_data['property_id']):
        property = Properties.objects.filter(id = post_data['property_id'])
        property.update(
        title = post_data['title'],
        price = post_data['price'],
        adddress = post_data['adddress'],
        county = post_data['county'],
        state = post_data['state'],
        city = post_data['city'],
        postal_code = post_data['postal_code'],
        content = post_data['content'],
        # dimensions
        area_unit = post_data['area_unit'],
        buildup_area_unit = post_data['buildup_area_unit'],
        buildup_area = post_data['buildup_area'],
        carpet_area = post_data['carpet_area'],
        carpet_area_unit = post_data['carpet_area_unit']
        )
        property = property[0]

        if len(post_data['video_link'])>1:
            property.video_link = post_data['video_link']
            
        # save images
        # main image
        try:
            b_64_converted = convert_base_to_raw(post_data['main_image'])
            file_name = f"{property.title}.jpg"
            property.main_image.save(file_name, b_64_converted['data'],save=True)
            property.save()
        except:
            pass

        # all images
        if len(post_data['all_images']) >= 1:
            update_property_images(property, post_data['all_images'])

        # features
        if len(post_data['features']) >= 1:
            update_property_features(property, post_data['features'])    
        
        # property type
        if len(post_data['type']) >= 1:
            update_property_types(property, post_data['type'])
        return JsonResponse({"message":'success'})


@csrf_exempt
def save_searches(request):
    body_unicode = request.body.decode('utf-8')
    post_data = json.loads(body_unicode)
    if accounts_views.getUser(request)['status'] == 200:
        user = accounts_views.getUser(request)['body']
        if not SavedSearch.objects.filter(user = user, city = post_data['city']).exists():
            SavedSearch(
                user = user,
                city = post_data['city']
            ).save()
        return JsonResponse({"message":'success'})
    else:
        return Response({'error': 'Profile Not found'}, status=400)

@csrf_exempt
def get_user_searches(request):
    body_unicode = request.body.decode('utf-8')
    post_data = json.loads(body_unicode)
    if accounts_views.getUser(request)['status'] == 200:
        user = accounts_views.getUser(request)['body']
        if SavedSearch.objects.filter(user = user).exists():
            searches_data = list(SavedSearch.objects.filter(user=user).values_list('city'))
        return JsonResponse(searches_data, safe=False)
    else:
        return Response({'error': 'Profile Not found'}, status=400)
    

@csrf_exempt
def get_user_listings(request):
    body_unicode = request.body.decode('utf-8')
    post_data = json.loads(body_unicode)
    if accounts_views.getUser(request)['status'] == 200:
        user = accounts_views.getUser(request)['body']
        properties = Properties.objects.filter(user = user).order_by('-pub_date')
        resp_data = listing_pagination(request,properties, post_data)   
        return JsonResponse(resp_data, safe=False)
    else:
        return Response({'error': 'Profile Not found'}, status=400)



