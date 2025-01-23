from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def recommend_products_cf(user):
    # Generate a user-item interaction matrix
    interactions = Interaction.objects.filter(user=user)
    product_ids = [interaction.product.id for interaction in interactions]
    interaction_matrix = np.zeros((len(product_ids), len(product_ids)))  # Example matrix
    
    for i in range(len(product_ids)):
        for j in range(len(product_ids)):
            if i != j:
                interaction_matrix[i, j] = cosine_similarity(
                    interaction_matrix[i, :].reshape(1, -1), 
                    interaction_matrix[j, :].reshape(1, -1)
                )

    # Fetch top N recommendations
    recommended_products = sorted(range(len(interaction_matrix)), key=lambda i: interaction_matrix[i])[:5]
    return recommended_products
