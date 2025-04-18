from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt




from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
import logging

#configure logging
logger = logging.getLogger(__name__)

# Create your views here. these are functions that handle different HTTP requests for the endpoints, they are thereforerelated to the endpoints
 
class LatestProductsList(APIView):
    def get(self, request, format=None):
        products= Product.objects.all()[0:4]
        serializer=ProductSerializer(products, many=True)
        return Response(serializer.data)
    logger.info(f"Response received for list of latest products")
    
class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)            #in this exerpt(4 lines), the get method: Handles GET requests, retrieves the product using get_object, serializes it, and returns the serialized data in an HTTP response.
        return Response(serializer.data)
    
class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug) #Retrieves a Category object based on the category slug,
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, format=None):
        category=self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
@csrf_exempt
@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})