from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.core.files.base import ContentFile
from io import BytesIO
from product_sug.models import CustomUser, Product
from .images import create_shirt_image, create_pants_image, create_vest_image, create_earrings_image, create_necklace_image, create_bangle_image, create_dress_image, create_skirt_image, create_shoes_image

fake = Faker()
class Command(BaseCommand):
    help = 'Generates fake data for users, products, interactions, and product suggestions'

    def handle(self, *args, **kwargs):
        

        # Helper function to get a random color
        def get_random_color():
            return random.choice(['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#000000', '#FFFFFF'])

        # Function to create fake products with images
        def create_fake_product():
            product_name = random.choice([product[0] for product in Product.PRODUCT_TYPES])
            category = random.choice([category[0] for category in Product.CATEGORY_CHOICES])
            description = fake.text(max_nb_chars=200)
            color = get_random_color()
            
            # Generate product image based on type
            if product_name == 'shirt':
                img = create_shirt_image(color)
            elif product_name == 'pants':
                img = create_pants_image(color)
            elif product_name == 'vest':
                img = create_vest_image(color)
            elif product_name == 'earrings':
                img = create_earrings_image(color)
            elif product_name == 'necklace':
                img = create_necklace_image(color)
            elif product_name == 'bangles':
                img = create_bangle_image(color)
            elif product_name == 'dress':
                img = create_dress_image(color)
            elif product_name == 'skirt':
                img = create_skirt_image(color)
            elif product_name == 'shoes':
                img = create_shoes_image(color)
            else:
                img = create_shirt_image(color)  # Default to shirt if type is not recognized

            # Save the image to an in-memory file
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)

            # Use ContentFile to simulate a file with a name
            img_file = ContentFile(img_byte_arr.read(), name=f"{product_name}_{random.randint(1, 1000)}.png")

            # Create and save the product in the database
            product = Product.objects.create(
                product_name=product_name,
                category=category,
                description=description,
                image=img_file,  # Save the ContentFile as the image
            )
            product.save()
            return product

        # Generate 10 fake products
        for _ in range(100):
            create_fake_product()

        print("Fake products with images have been generated.")