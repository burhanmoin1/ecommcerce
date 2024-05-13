from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.http import JsonResponse
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .mongobackend import MongoEngineBackend
from datetime import datetime
from django.contrib.auth import login
import uuid
from django.forms.models import model_to_dict
import json
from brand.models import *
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password

@api_view(['POST'])
def addsuperuser(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if not username or not email or not password:
            return Response(
                {'error': 'Username, email, and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if SuperUser.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if SuperUser.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        superuser = SuperUser(email=email, password=password, username=username)
        superuser.save()

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def loginsuperuser(request):
    if request.method == 'POST':
        data = request.data
        login_input = data.get('login')  # The single input field for email or username
        password = data.get('password')

        # Initialize to None
        superuser = None

        if "@" in login_input:
            superuser = MongoEngineBackend().authenticate(request, login=login_input, password=password)
        else:
            superuser = MongoEngineBackend().authenticate(request, login=login_input, password=password)

        if superuser and superuser.is_superuser:
            # Log the superuser in
            login(request, superuser)

            sessions = SuperUserSession.objects.filter(superuser=superuser, is_active=True)

            # If there are more than two active sessions, delete the oldest
            if sessions.count() > 1:
                sessions = sessions.order_by('created_at')  # Sort sessions by creation time
                sessions[0].delete()

            superuser.login_time = datetime.now()  # Log the login time
            superuser.save()  # Save changes to the superuser

            session_id = str(uuid.uuid4())

            user_session = SuperUserSession(
                superuser=superuser,
                session_id=session_id,
                created_at=datetime.now(),
                last_activity=datetime.now(),
                is_active=True
            )
            user_session.save() 

            # Return success message
            return JsonResponse({
                'session_id': session_id,
                'message': 'Login successful'
            }, status=200)  # Status 200 for successful login

        else:
            return JsonResponse(
                {'error': 'Invalid email/username or password, or account not activated.'},
                status=400  # Status 400 for client error
            )

    # If not POST method, return method not allowed
    return JsonResponse({'error': 'Method Not Allowed'}, status=405)

@api_view(['POST'])
def adminsessionchecker(request):
    if request.method == 'POST':
        data = request.data
        session_id = data.get('session_id')
        
        if SuperUserSession.objects.filter(session_id=session_id).exists():
            return JsonResponse({'message': 'Session authentiated'}, status=200)

        else:
            return JsonResponse(
                {'error': 'session_id not authenticated'},
                status=400  # Status 400 for client error
            )
        
    return JsonResponse({'error': 'Method Not Allowed'}, status=405)


@api_view(['GET'])
def BrandFormView(request):
    # Ensure this endpoint is for GET requests only
    if request.method != 'GET':
        return Response({'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Fetch session ID from query parameters or data
    session_id = request.GET.get('session_id', request.data.get('session_id'))

    if not session_id:
        return Response({'error': 'Session ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

    if not SuperUserSession.objects.filter(session_id=session_id).exists():
        return Response({'error': 'Session not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    brand_id = request.GET.get('brand_id', request.data.get('brand_id'))  # Fetch brand_id from query parameters

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
            return Response(serialized_data, status=status.HTTP_200_OK)
        except BrandForm.DoesNotExist:
            return Response({'error': 'Brand not found'}, status=status.HTTP_404_NOT_FOUND)

    else:
        # Get all BrandForm instances
        brands = BrandForm.objects.all()  # Retrieve all instances
        # Convert the list to a dictionary
        serialized_data = [
            {**model_to_dict(brand), '_id': str(brand.id)} for brand in brands
        ]
        return Response(serialized_data, status=status.HTTP_200_OK)

class AddPrimaryCategory(APIView):
    def get(self, request, *args, **kwargs):
        primary_categories = PrimaryCategory.objects.all()
        serialized_data = [
            {
                'id': str(primary.id),  # Convert ObjectId to string
                'name': primary.name,
                # Add any other fields you need
            }
            for primary in primary_categories
        ]
        return Response(serialized_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        primary_category_name = request.data.get("name")
        primary_category_description = request.data.get("description")
        if not primary_category_name or not primary_category_description:
            return Response({'error': 'Name and description are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Check if the primary category already exists
            if PrimaryCategory.objects.filter(name=primary_category_name).exists():
                return Response({'error': 'Primary category already exists'}, status=status.HTTP_409_CONFLICT)

            # Create the primary category
            primary_category = PrimaryCategory(name=primary_category_name, description=primary_category_description)
            primary_category.save()

            return Response({'message': 'Primary category added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddSecondaryCategory(APIView):
    def post(self, request, *args, **kwargs):
        secondary_category_name = request.data.get("name")
        secondary_category_description = request.data.get("description")
        parent_category_id = request.data.get("parent_category_id")

        if not secondary_category_name or not secondary_category_description or not parent_category_id:
            return Response({'error': 'Name, description, and parent category ID are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the parent category exists
            parent_category = PrimaryCategory.objects.get(id=parent_category_id)

            # Create the secondary category
            secondary_category = SecondaryCategory(name=secondary_category_name, description=secondary_category_description, parent_category=parent_category)
            secondary_category.save()

            return Response({'message': 'Secondary category added successfully'}, status=status.HTTP_201_CREATED)
        except PrimaryCategory.DoesNotExist:
            return Response({'error': 'Parent category does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

