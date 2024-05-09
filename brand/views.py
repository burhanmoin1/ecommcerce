from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from superuser.views import *

def brandform(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            new_brand = BrandForm(
                brand_name=data.get('brand_name'),
                person_name=data.get('person_name'),
                email=data.get('email'),
                phone_number=data.get('phone_number'),
                city=data.get('city'),
                social_media_presence=data.get('social_media_presence'),
                brands_business_operations=data.get('brands_business_operations'),
                brands_product_category=data.get('brands_product_category'),
                catalog_size=data.get('catalog_size'),
                price_range=data.get('price_range'),
                supply_chain=data.get('supply_chain'),
                inventory=data.get('inventory'),
                star_rating=data.get('star_rating'),
                feedback_text=data.get('feedback_text'),
                website=data.get('website'),
            )

            new_brand.save()

            serialized_data = {
                '_id': str(new_brand.id),
                'brand_name': new_brand.brand_name,
                'person_name': new_brand.person_name,
                'email': new_brand.email,
                'phone_number': new_brand.phone_number,
                'city': new_brand.city,
                'social_media_presence': new_brand.social_media_presence,
                'brands_business_operations': new_brand.brands_business_operations,
                'brands_product_category': new_brand.brands_product_category,
                'catalog_size': new_brand.catalog_size,
                'price_range': new_brand.price_range,
                'supply_chain': new_brand.supply_chain,
                'inventory': new_brand.inventory,
                'star_rating': new_brand.star_rating,
                'feedback_text': new_brand.feedback_text,
                'website': new_brand.website,
            }

            return JsonResponse(serialized_data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

class BrandFormView(APIView):
    """Class-based view to handle BrandForm with session authentication."""
    
    permission_classes = [IsSessionAuthenticated]  # Apply custom session-based permission

    def get(self, request, brand_id=None):
        if brand_id:
            # Get a specific BrandForm by ID
            try:
                brand = BrandForm.objects.get(id=brand_id)
                # Convert the BrandForm to a dictionary for the JSON response
                serialized_data = {
                    '_id': str(brand.id),
                    'brand_name': brand.brand_name,
                    'person_name': brand.person_name,
                    'email': brand.email,
                    'phone_number': brand.phone_number,
                    'city': brand.city,
                    'social_media_presence': brand.social_media_presence,
                    'brands_business_operations': brand.brands_business_operations,
                    'brands_product_category': brand.brands_product_category,
                    'catalog_size': brand.catalog_size,
                    'price_range': brand.price_range,
                    'supply_chain': brand.supply_chain,
                    'inventory': brand.inventory,
                    'star_rating': brand.star_rating,
                    'feedback_text': brand.feedback_text,
                    'website': brand.website,
                }
                return Response(serialized_data, status=status.HTTP_200_OK)  # HTTP 200 OK
            except BrandForm.DoesNotExist:
                return Response({'error': 'Brand not found'}, status=status.HTTP_404_NOT_FOUND)  # HTTP 404

        else:
            # Get all BrandForm instances
            brands = BrandForm.objects.all()  # Retrieve all instances
            # Convert the list to a dictionary
            serialized_data = [
                {**model_to_dict(brand), '_id': str(brand.id)} for brand in brands
            ]
            return Response(serialized_data, status=status.HTTP_200_OK) 
