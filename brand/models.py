from django_mongoengine import Document, fields
from datetime import datetime
import os

class BrandForm(Document):
    brand_name = fields.StringField(max_length=255, blank=False, unique=True)  # No blanks allowed
    person_name = fields.StringField(max_length=255, blank=False)
    email = fields.EmailField(max_length=255, blank=False, unique=True)
    phone_number = fields.StringField(max_length=255, blank=False)
    city = fields.StringField(max_length=255, blank=False)
    social_media_presence = fields.BooleanField(default=False)  # Default to False
    brands_business_operations = fields.StringField(max_length=255, blank=False)
    brands_product_category = fields.StringField(max_length=255, blank=False)
    catalog_size = fields.StringField(blank=False)
    price_range = fields.StringField(blank=False)
    supply_chain = fields.StringField(max_length=255, blank=False)
    inventory = fields.StringField(max_length=255, blank=False)
    star_rating = fields.StringField(blank=False)  # Use correct namespace for IntField
    feedback_text = fields.StringField(blank=True)  # Allow blank feedback
    website = fields.URLField(max_length=255, blank=False, unique=True)

class BrandAccount(Document):
    email = fields.EmailField(blank=False, unique=True)
    password = fields.StringField(blank=False)
    is_verified = fields.BooleanField(default=False)
    login_time = fields.DateTimeField(blank=True)
    session_token = fields.StringField(blank=True)
    brand_name = fields.StringField(blank=True)

class BrandAccountSession(Document):
    brandaccount = fields.ReferenceField(BrandAccount, blank=False)
    session_id = fields.StringField(unique=True) 
    created_at = fields.DateTimeField(default=datetime.now)
    last_activity = fields.DateTimeField(default=datetime.now)
    is_active = fields.BooleanField(default=True)

class PrimaryCategory(Document):
    name = fields.StringField(blank=False, unique=True)
    description = fields.StringField(blank=False)

class SecondaryCategory(Document):
    name = fields.StringField(blank=False)
    description = fields.StringField(blank=False)
    parent_category = fields.ReferenceField(PrimaryCategory, blank=False)

class ProductColors(Document):
    name = fields.StringField(blank=False)

class ProductSizes(Document):
    name = fields.StringField(blank=False)

class Product(Document):
    name = fields.StringField(blank=False, unique=True)
    description = fields.StringField(blank=False)
    sku = fields.StringField(blank=False, unique=True)
    primary_category = fields.ReferenceField(PrimaryCategory, blank=False)
    secondary_category = fields.ReferenceField(SecondaryCategory, blank=False)
    brand_account = fields.ReferenceField(BrandAccount, blank=False)
    price = fields.StringField(blank=False)

class ProductVariation(Document):
    product = fields.ReferenceField(Product, blank=False)
    color = fields.StringField(blank=False)
    size = fields.StringField(blank=False)
    quantity = fields.StringField(blank=False)

    meta = {
        'indexes': [
            {'fields': ['product', 'color', 'size'], 'unique': True}
        ]
    }

    def generate_sku(self):
        # Concatenate parent product's SKU with color
        return f"{self.product.sku}-{self.color}"

class ProductVariationImage(Document):
    product_variation = fields.ReferenceField(ProductVariation, blank=False, related_name='productvariationimages')
    image = fields.ImageField()

    def generate_sku(self):
        # Access the related product_variation and call its generate_sku method
        return self.product_variation.generate_sku()

    def get_upload_path(instance, filename):
        # Get the SKU generated by the product variation
        sku = instance.generate_sku()
        # Create the directory path
        directory_path = os.path.join('productvariation', sku)
        # Return the full upload path
        return os.path.join(directory_path, filename)

    meta = {
        'indexes': [
            {'fields': ['product_variation'], 'unique': True}
        ],
        'allow_inheritance': True
    }

    # Override the upload_to parameter
    image = fields.ImageField(upload_to=get_upload_path)



    