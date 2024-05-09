from django_mongoengine import Document, fields

class BrandAccount(Document):
    email = fields.EmailField(blank=False, unique=True)
    password = fields.StringField(blank=False)
    password_reset_token = fields.StringField(blank=True)
    session_token = fields.StringField(blank=True)

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
