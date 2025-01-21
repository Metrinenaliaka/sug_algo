from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Interaction, UserPreferences
from .serializers import ProductSerializer, InteractionSerializer, UserPreferencesSerializer
from .utils import update_user_preferences


# View to upload products
class ProductUploadView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product uploaded successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View to handle user interactions (like, dislike, view)
class UserInteractionView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')
        interaction_type = request.data.get('interaction_type')
        interaction_count = request.data.get('interaction_count', 1)

        # Validate the interaction data
        if not all([user_id, product_id, interaction_type]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        # Create or update the interaction
        user = CustomUser.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
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

        # Update the user's preferences after each interaction
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

