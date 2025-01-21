from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status, generics
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Interaction, UserPreferences, CustomUser
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer, InteractionSerializer, UserPreferencesSerializer, CustomUserSerializer
from .utils import update_user_preferences
from rest_framework.permissions import IsAuthenticated

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        # Return user data
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email
        })

class SignupView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()  # Create the user
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user using Django's authentication system
        user = authenticate(username=username, password=password)

        if user is not None:
            # Log the user in using Django's session system
            login(request, user)

            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# View to upload products
class ProductUploadView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product uploaded successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductFilter(django_filters.FilterSet):
    # Filter by product name (e.g., shirt, pants)
    product_name = django_filters.CharFilter(field_name='product_name', lookup_expr='icontains')
    
    # Filter by category (e.g., clothing, accessory)
    category = django_filters.CharFilter(field_name='category', lookup_expr='icontains')
    
    # You can add more filters based on other fields as needed.
    class Meta:
        model = Product
        fields = ['product_name', 'category']

class ProductPagination(PageNumberPagination):
    page_size = 10  # Number of products per page
    page_size_query_param = 'page_size'  # Allow clients to change the page size with a query parameter
    max_page_size = 100  # Maximum allowed page size

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()  # Retrieve all products
    serializer_class = ProductSerializer  # Use the ProductSerializer to serialize the data

    
    
    # # Apply filtering using DjangoFilterBackend and the ProductFilter class
    # filter_backends = (DjangoFilterBackend, django_filters.OrderingFilter)
    # filterset_class = ProductFilter  # Use the ProductFilter class
    
    # # Add ordering functionality
    # ordering_fields = ['product_name', 'category', 'created_at', 'price']
    # ordering = ['created_at']  # Default ordering by created_at
    
    # # Add pagination
    # pagination_class = ProductPagination

# View to handle user interactions (like, dislike, view)
class UserInteractionView(APIView):
    def post(self, request):
        # Use the logged-in user (request.user)
        user = request.user

        # If the user is not authenticated, return an error
        if not user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the product_id and interaction_type from the request data
        product_id = request.data.get('product_id')
        interaction_type = request.data.get('interaction_type')
        interaction_count = request.data.get('interaction_count', 1)

        # Validate the interaction data
        if not all([product_id, interaction_type]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate that interaction type is either 'like' or 'dislike'
        if interaction_type not in ['like', 'dislike']:
            return Response({"error": "Invalid interaction type."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the product from the database
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Create or update the interaction
        interaction, created = Interaction.objects.get_or_create(
            user=user,
            product=product,
            interaction_type=interaction_type,
            defaults={'interaction_count': interaction_count}
        )
        
        if not created:
            # If the interaction already exists, increment the interaction count
            interaction.interaction_count += interaction_count
            interaction.save()

        # Optionally, update the user's preferences after each interaction
        update_user_preferences(user)

        return Response({"message": "Interaction recorded successfully!"}, status=status.HTTP_200_OK)


# View to get product recommendations for a user
class ProductRecommendationView(APIView):
    def get(self, request, user_id):
        # Fetch user preferences
        user = CustomUser.objects.get(id=user_id)
        preferences = UserPreferences.objects.filter(user=user)
        
        if preferences.exists():
            # Get the top recommended products based on user's preferences
            preferred_type = preferences.first().preferred_product_type
            preferred_description = preferences.first().preferred_description

            recommended_products = Product.objects.filter(product_name=preferred_type, description=preferred_description)
            serializer = ProductSerializer(recommended_products, many=True)
            return Response(serializer.data)
        
        return Response({"message": "No preferences found for this user."}, status=status.HTTP_404_NOT_FOUND)

