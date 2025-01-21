from django.urls import path
from .views import ProductUploadView, UserInteractionView, ProductRecommendationView

urlpatterns = [
    path('upload_product/', ProductUploadView.as_view(), name='upload_product'),
    path('user_interaction/', UserInteractionView.as_view(), name='user_interaction'),
    path('product_recommendations/<int:user_id>/', ProductRecommendationView.as_view(), name='product_recommendations'),
]
