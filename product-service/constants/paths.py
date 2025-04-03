import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Media directories within static
IMAGES_DIR = os.path.join(STATIC_DIR, "images")
CATEGORY_IMAGES_DIR = os.path.join(IMAGES_DIR, "categories")

PRODUCT_IMAGES_DIR = os.path.join(IMAGES_DIR, "products")
LEVEL_ONE_IMAGES_DIR = os.path.join(CATEGORY_IMAGES_DIR, "level-one")
LEVEL_TWO_IMAGES_DIR = os.path.join(CATEGORY_IMAGES_DIR, "level-two")
LEVEL_THREE_IMAGES_DIR = os.path.join(CATEGORY_IMAGES_DIR, "level-three")


COLOR_IMAGES_DIR = os.path.join(IMAGES_DIR, "colors")

# Create directories if they don't exist
for directory in [STATIC_DIR, IMAGES_DIR, PRODUCT_IMAGES_DIR, COLOR_IMAGES_DIR, 
                  CATEGORY_IMAGES_DIR, LEVEL_ONE_IMAGES_DIR, 
                  LEVEL_TWO_IMAGES_DIR, LEVEL_THREE_IMAGES_DIR]:
    os.makedirs(directory, exist_ok=True) 