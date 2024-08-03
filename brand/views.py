from django.shortcuts import render
from django.http import JsonResponse
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .mongobackend import MongoEngineBackend
from .models import *
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
import uuid

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


@api_view(['POST'])
def addbrandaccount(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(
                {'error': 'Email, and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        hashed_password = make_password(password)

        if BrandAccount.objects.filter(email=email).exists():
            return Response({'error': 'Brand with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        brandaccount = BrandAccount(email=email, password=hashed_password)
        brandaccount.save()

        return Response({'message': 'Brand Account created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def BrandAccountLogin(request):
    if request.method == 'POST':
        data = request.data
        email = data.get('email')
        password = data.get('password')
        brandaccount = MongoEngineBackend().authenticate(request, email=email, password=password)

        if brandaccount and brandaccount.is_verified:
            # Log the superuser in
            login(request, brandaccount)

            sessions = BrandAccountSession.objects.filter(brandaccount=brandaccount, is_active=True)

            # If there are more than two active sessions, delete the oldest
            if sessions.count() > 1:
                sessions = sessions.order_by('created_at')  # Sort sessions by creation time
                sessions[0].delete()

            brandaccount.login_time = datetime.now()  # Log the login time
            brandaccount.save()  # Save changes to the superuser

            session_id = str(uuid.uuid4())

            brand_session = BrandAccountSession(
                brandaccount=brandaccount,
                session_id=session_id,
                created_at=datetime.now(),
                last_activity=datetime.now(),
                is_active=True
            )
            brand_session.save() 

            # Return success message
            return JsonResponse({
            'session_id': session_id,
            'message': 'Login successful',
            'brand_account': {
                'brand_name': brandaccount.brand_name,
                'id': str(brandaccount.id)
            }
        }, status=200)

        else:
            return JsonResponse(
                {'error': 'Invalid email/username or password, or account not activated.'},
                status=400  # Status 400 for client error
            )

    # If not POST method, return method not allowed
    return JsonResponse({'error': 'Method Not Allowed'}, status=405)


@api_view(['POST'])
def brandaccountsessionchecker(request):
    if request.method == 'POST':
        data = request.data
        session_id = data.get('session_id')
        
        if BrandAccountSession.objects.filter(session_id=session_id).exists():
            return JsonResponse({'message': 'Session authentiated'}, status=200)

        else:
            return JsonResponse(
                {'error': 'session_id not authenticated'},
                status=400  # Status 400 for client error
            )
        
    return JsonResponse({'error': 'Method Not Allowed'}, status=405)

class BrandProductsforDashboard(APIView):
    def get(self, request, brand_name, *args, **kwargs):
        # Assuming BrandAccount model is defined somewhere
        
        # Fetch the BrandAccount object based on the provided brand_name
        try:
            brand_account = BrandAccount.objects.get(name=brand_name)
        except BrandAccount.DoesNotExist:
            return Response({"error": "Brand not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Fetch all products associated with the brand
        products = Product.objects.filter(brand_name=brand_account)
        
        # Serialize product data
        serialized_data = [
            {
                'name': product.name,
                'description': product.description,
                'sku': product.sku,
                'primary_category': str(product.primary_category.id),
                'secondary_category': str(product.secondary_category.id),
                'brand_name': str(product.brand_name.id),
                'price': str(product.price),
            }
            for product in products
        ]
        
        return Response(serialized_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Assuming the request data contains the necessary information for creating a product
        data = request.data
        try:
            # Assuming brand_name is provided in the request data
            product = Product(
                name=data('name'),
                description=data('description'),
                sku=data('sku'),
                primary_category=data('primary_category'),
                secondary_category=data('secondary_category'),
                brand_account=data('brand_name'),
                price=data('price')
            )

            product.save()
            return Response({"message": "Product created successfully"}, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({"error": f"Missing required field: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_secondary_categories(request):
    if request.method == 'GET':
        primary_category_name = request.GET.get('primary_category_name')

        try:
            primary_category = PrimaryCategory.objects.get(name=primary_category_name)
            secondary_categories = SecondaryCategory.objects.filter(parent_category=primary_category)

            secondary_categories_data = [{
                'id': str(category.id),
                'name': category.name,
                'description': category.description
            } for category in secondary_categories]

            return JsonResponse({'secondary_categories': secondary_categories_data})
        except PrimaryCategory.DoesNotExist:
            return JsonResponse({'error': 'Primary category does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
class ProductVariationImageView(APIView):
    def post(self, request, *args, **kwargs):
        
        product_variation_id = request.data.get('product_variation_id')
        image = request.data.get('image')

        # Check if required fields are present
        if not product_variation_id or not image:
            return Response({'error': 'product_variation_id and image are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the ProductVariation instance
            product_variation = ProductVariation.objects.get(id=product_variation_id)
        except ProductVariation.DoesNotExist:
            return Response({'error': 'ProductVariation not found'}, status=status.HTTP_404_NOT_FOUND)

        # Save the image to the productvariation/{generate.sku} directory
        try:
            ProductVariationImage.objects.create(product_variation=product_variation, image=image)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Image uploaded successfully'}, status=status.HTTP_201_CREATED)