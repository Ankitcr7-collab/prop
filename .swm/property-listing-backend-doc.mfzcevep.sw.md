---
title: Property Listing Backend Doc
---
<SwmSnippet path="accounts/views.py" line="40">

---

Facebook Login View

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

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBcHJvcCUzQSUzQUFua2l0Y3I3LWNvbGxhYg==" repo-name="prop"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
