from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import FacebookLogin, GoogleLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user-accounts/', include('accounts.urls')),
    path('listings/', include('listings.urls')),
    # path('accounts/', include('allauth.urls'))
    path('user-accounts/', include('dj_rest_auth.urls')),
    path('user-accounts/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('user-accounts/google/', GoogleLogin.as_view(), name='google_login'),
    path('accounts/', include('allauth.urls'), name='socialaccount_signup'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)