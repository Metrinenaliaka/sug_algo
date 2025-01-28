from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO

# Function to create a shirt image
def create_shirt_image(color, pattern=None):
    width, height = 400, 500
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    # Draw shirt shape (rectangle base with collar)
    draw.rectangle([50, 50, 350, 450], fill=color)
    draw.rectangle([150, 20, 250, 50], fill=random.choice(['#000000', '#FFFFFF', '#B22222']))  # Collar
    if pattern == 'stripes':
        for i in range(0, width, 20):
            draw.line([(i, 50), (i + 50, height)], fill='black', width=5)
    return img

# Function to create pants image
def create_pants_image(color):
    width, height = 400, 500
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    # Draw pants shape (rectangular body with legs)
    draw.rectangle([100, 50, 300, 350], fill=color)
    draw.rectangle([100, 350, 150, 450], fill=color)  # Left leg
    draw.rectangle([250, 350, 300, 450], fill=color)  # Right leg
    return img

# Function to create a vest image
def create_vest_image(color):
    width, height = 400, 500
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    # Draw vest shape (rectangle with cut-out arms)
    draw.rectangle([50, 50, 350, 450], fill=color)
    draw.rectangle([50, 100, 150, 450], fill='white')  # Left armhole
    draw.rectangle([250, 100, 350, 450], fill='white')  # Right armhole
    return img

# Function to create earrings image
def create_earrings_image(color):
    width, height = 200, 200
    img = Image.new('RGBA', (width, height), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    # Draw earrings (simple circles)
    draw.ellipse([50, 50, 150, 150], fill=color, outline='black')
    return img

# Function to create necklace image
def create_necklace_image(color):
    width, height = 400, 200
    img = Image.new('RGBA', (width, height), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    # Draw necklace (simple curved line with beads)
    draw.arc([50, 50, 350, 150], start=0, end=180, fill=color, width=5)
    for x in range(100, 350, 50):
        draw.circle([x, 100], radius=10, fill='gold')  # Adding beads
    return img

# Function to create bangle image
def create_bangle_image(color):
    width, height = 200, 200
    img = Image.new('RGBA', (width, height), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    # Draw a bangle (circle shape)
    draw.ellipse([50, 50, 150, 150], fill=color, outline='black')
    return img

# Function to create dress image
def create_dress_image(color):
    width, height = 400, 500
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    # Draw dress shape (rectangle with flared bottom)
    draw.rectangle([100, 50, 300, 350], fill=color)
    draw.polygon([(100, 350), (300, 350), (250, 450), (150, 450)], fill=color)
    return img

# Function to create skirt image
def create_skirt_image(color):
    width, height = 400, 500
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    # Draw skirt (trapezoid shape)
    draw.polygon([(50, 50), (350, 50), (300, 450), (100, 450)], fill=color)
    return img

# Function to create shoes image
def create_shoes_image(color):
    width, height = 400, 200
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    # Draw shoes (simple rectangular base with toe cap)
    draw.rectangle([50, 50, 350, 150], fill=color)
    draw.ellipse([150, 120, 250, 180], fill='darkgray')
    return img

