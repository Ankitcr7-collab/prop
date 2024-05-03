---
title: Property Listing Accounts app
---
<SwmSnippet path="accounts/views.py" line="40">

---

**Facebook Login View**

This code snippet is a part of a class named `FacebookLogin` that inherits from `SocialLoginView`. It sets the `adapter_class` attribute to `FacebookOAuth2Adapter` and the `client_class` attribute to `OAuth2Client`. The `process_login` method sets the `backend` attribute of the `user` object in the `request` to `'django.contrib.auth.backends.ModelBackend'`, calls the `login` function with the `request` and `user` arguments, and then retrieves the access token for the `user` using the `get_tokens_for_user` function and stores it in the `access_token` variable.

```
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client

    def process_login(self):
        self.request.user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, self.user)
        access_token = get_tokens_for_user(self.request.user)['access']
```

---

</SwmSnippet>

<SwmSnippet path="/accounts/views.py" line="52">

---

**Google Login view**

This code is a class that extends `SocialLoginView` and provides a Google login functionality. It sets the permission classes to allow any user, uses the `GoogleOAuth2Adapter` adapter class, and the `OAuth2Client` client class. It also defines a `process_login` method that sets the user's backend, logs in the user, retrieves an access token for the user, and returns a response with the access token.

```python
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
```

---

</SwmSnippet>

<SwmSnippet path="/accounts/views.py" line="91">

---

**User registration view handler**

This code snippet defines a class `UserRegister` that is a subclass of `APIView`. It has a `post` method that handles the POST requests. It sets the `permission_classes` attribute to allow any user to access the endpoint. Inside the `post` method, it creates an instance of `UserRegisterSerializer` and validates the data. If the data is valid, it calls the `create` method of the serializer to create a new user. If the user is created successfully, it returns a response with the serialized user data and the HTTP status code 201 (Created). If the data is not valid, it returns a response with a message indicating invalid credentials and the HTTP status code 400 (Bad Request).

```python
class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)

            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

```

---

</SwmSnippet>

<SwmSnippet path="/accounts/views.py" line="118">

---

This code snippet defines a function `getUser` that takes a `request` object as an argument. It extracts a token from the `HTTP_AUTHORIZATION` header of the request, decodes it using the `TokenBackend` algorithm with an option to not verify the token. If the decoding is successful, it retrieves the `user_id` from the decoded data. The function then checks if a `User` object with the specified `user_id` exists in the database. If it exists, it returns a response with a status code of 200 and the corresponding `User` object. If the `User` does not exist, it returns a response with a status code of 400 and a message indicating that the user was not found.

```python
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
    
```

---

</SwmSnippet>

<SwmSnippet path="/accounts/views.py" line="179">

---

**User Login View Handler**

This code snippet is a `LoginView` class that inherits from `TokenObtainPairView`. It handles the `POST` request for user login. The `permission_classes` attribute is set to allow any user. The `post` method receives the request data, validates it using a `UserLoginSerializer`, and checks if the user exists. If the user exists, it logs in the user, generates an access token using `get_tokens_for_user`, and returns a response with the access token. If the user doesn't exist, it returns a response with an error message. If the serializer is invalid, it returns a response with an error message.

```python
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

```

---

</SwmSnippet>

<SwmSnippet path="/accounts/views.py" line="291">

---

**Update User profile**

```python
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
  
```

---

</SwmSnippet>

<SwmSnippet path="/accounts/views.py" line="280">

---

**Image format handling view**

This code snippet defines a `convert_base_to_raw` function that takes two arguments: `user` and `img_data`. It splits the `img_data` string into `format` and `imgstr` using the ';base64,' separator. It then splits the `format` string to extract the file extension (`ext`). The `imgstr` is base64-decoded and saved as a `ContentFile` object with the name 'temp.' + `ext`. Finally, it generates a `file_name` by concatenating the `user.username` and `ext`, and returns a dictionary with the `file_name` and `data`.

```python
def convert_base_to_raw(user, img_data):
    format, imgstr = img_data.split(';base64,') 
    ext = format.split('/')[-1]     
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    file_name = f"{user.username}." + ext
    return {
        'file_name':file_name,
        'data':data
    }

```

---

</SwmSnippet>

<SwmSnippet path="/accounts/views.py" line="242">

---

**Public profile**

This code snippet defines a class `GerPublicProfile` that extends `CsrfExempt` and `APIView`. It provides a `post` method that takes a `request` object and decodes the request body. It then checks if a `User` object with the given `user_id` exists. If it does, it retrieves the corresponding `UserProfile` object and generates a JSON response containing the profile data using the `profile_json` function. If the `User` object does not exist, it returns a response with an error message.

```python
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
```

---

</SwmSnippet>

<SwmSnippet path="/accounts/views.py" line="205">

---

**Profile json data**

This code snippet defines a function `profile_json` that generates a JSON object containing user and profile details. The function takes in a `request` object, `user_queryset` and `profile_queryset` as parameters, along with a boolean `is_properties`. It first checks the user's role using the `check_userrole` function. Then, it creates a list `properties_data` and initializes a `jsonData` dictionary with user details such as email, first name, last name, etc. It also includes the user's profile picture and company logo URLs. If `is_properties` is true and the user has associated properties, it iterates over each property and fetches their details using the `get_property_details_json` function. These details are appended to the `properties_data` list. Finally, the `jsonData` dictionary is returned.

```python
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

```

---

</SwmSnippet>

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBcHJvcCUzQSUzQUFua2l0Y3I3LWNvbGxhYg==" repo-name="prop"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
