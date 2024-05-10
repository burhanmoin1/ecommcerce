from django_mongoengine import Document, fields
from datetime import datetime

class BrandForm(Document):
    brand_name = fields.StringField(max_length=255, blank=False, unique=True)  # No blanks allowed
    person_name = fields.StringField(max_length=255, blank=False)
    email = fields.EmailField(max_length=255, blank=False, unique=True)
    phone_number = fields.StringField(max_length=255, blank=False, unique=True)
    city = fields.StringField(max_length=255, blank=False)
    social_media_presence = fields.BooleanField(default=False)  # Default to False
    brands_business_operations = fields.StringField(max_length=255, blank=False)
    brands_product_category = fields.StringField(max_length=255, blank=False)
    catalog_size = fields.IntField(blank=False)
    price_range = fields.IntField(blank=False)
    supply_chain = fields.StringField(max_length=255, blank=False)
    inventory = fields.StringField(max_length=255, blank=False)
    star_rating = fields.IntField(blank=False)  # Use correct namespace for IntField
    feedback_text = fields.StringField(blank=True)  # Allow blank feedback
    website = fields.URLField(max_length=255, blank=False, unique=True)

class BrandAccount(Document):
    email = fields.EmailField(blank=False, unique=True)
    password = fields.StringField(blank=False)
    is_verified = fields.BooleanField(default=False)
    login_time = fields.DateTimeField(blank=True)
    session_token = fields.StringField(blank=True)
    brand_name = fields.ReferenceField(BrandForm, blank=False)

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
    name = fields.StringField(blank=False, unique=True)
    description = fields.StringField(blank=False)
    parent_category = fields.ReferenceField(PrimaryCategory, blank=False)

class ProductColors(Document):
    name = fields.StringField(blank=False)

class ProductSizes(Document):
    name = fields.StringField(blank=False)

class Product(Document):
    name = fields.StringField(blank=False)
    description = fields.StringField(blank=False)
    primary_category = fields.ReferenceField(PrimaryCategory, blank=False)
    secondary_category = fields.ReferenceField(SecondaryCategory, blank=False)
    brand_name = fields.ReferenceField(BrandAccount, blank=False)
    price = fields.DecimalField(blank=False)

class ProductVariation(Document):
    product = fields.ReferenceField(Product, blank=False)
    color = fields.ReferenceField(ProductColors, blank=False)
    size = fields.ReferenceField(ProductSizes, blank=False)
    quantity = fields.IntField(blank=False)




    