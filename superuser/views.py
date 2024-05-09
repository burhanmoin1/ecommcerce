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

class IsSessionAuthenticated(BasePermission):
    """Custom permission class to check if a session is authenticated."""

    def has_permission(self, request, view):
        # Extract session ID from the request data, headers, or another source
        session_id = request.data.get('session_id')  # Example of session ID extraction from request data
        # You can also extract from headers, cookies, etc.

        if not session_id:
            raise PermissionDenied('Session ID is required')  # Reject if no session ID is provided

        # Check if the session ID exists in the UserSession model and is valid
        if UserSession.objects.filter(session_id=session_id).exists():
            return True  # Allow access if the session is authenticated

        raise PermissionDenied('Session not authenticated')

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

            sessions = UserSession.objects.filter(superuser=superuser, is_active=True)

            # If there are more than two active sessions, delete the oldest
            if sessions.count() > 1:
                sessions = sessions.order_by('created_at')  # Sort sessions by creation time
                sessions[0].delete()

            superuser.login_time = datetime.now()  # Log the login time
            superuser.save()  # Save changes to the superuser

            session_id = str(uuid.uuid4())

            user_session = UserSession(
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
        
        if UserSession.objects.filter(session_id=session_id).exists():
            return JsonResponse({'message': 'Session authentiated'}, status=200)

        else:
            return JsonResponse(
                {'error': 'session_id not authenticated'},
                status=400  # Status 400 for client error
            )
        
    return JsonResponse({'error': 'Method Not Allowed'}, status=405)



class BrandFormView(APIView):
    """Class-based view to handle BrandForm with session authentication."""
    
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
