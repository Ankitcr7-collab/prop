from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('get-all-listings', views.get_all_listings, name='get_all_listings'),
    path('get-all-features', views.get_all_features, name='get_all_features'),
    path('get-listing-details', views.get_property_details, name='get_property_details'),
    path('search-listings', views.property_search, name='property_search'),
    path('order-listings', views.order_listings, name='order_listings'),
    path('add-listing', views.add_property, name='add_listing'),
    path('update-listing', views.update_property, name='update_listing'),
    path('save-searches', views.save_searches, name='save_searches'),
    path('get-user-searches', views.get_user_searches, name='get_user_searches'),
    path('get-user-listings', views.get_user_listings, name='get_user_listings'),
] 
