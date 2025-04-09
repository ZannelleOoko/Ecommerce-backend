
from django.urls import path, include
from product import views

#this is better than using "from .views import LatestProductlist" because we are going to be using multiple views, so it makes it easier to import all the view funcions rather than just one specific view function


urlpatterns=[
    path('latest-products/', views.LatestProductsList.as_view()),
    path('products/search/', views.search), #this url has to be placed here otherwise the endpoint does not work
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
   
]

