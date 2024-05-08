from django_mongoengine import Document, fields

class ConstrainedIntField(fields.IntField, MinMaxMixin):
    def __init__(self, *args, **kwargs):
        kwargs['min_value'] = 1  # Minimum value of 1
        kwargs['max_value'] = 5  # Maximum value of 5
        super().__init__(*args, **kwargs)

class BrandAccount(Document):
    brand_name = fields.StringField(max_length=255, required=True, unique=True)
    person_name = fields.StringField(max_length=255, required=True)
    email = fields.EmailField(max_length=255, required=True, unique=True)
    phone_number = fields.StringField(max_length=255, required=True, unique=True)
    city = fields.StringField(max_length=255, required=True)
    social_media_presence = fields.BooleanField(default=False)
    brands_business_operations = fields.StringField(max_length=255, required=True)
    brands_product_category = fields.StringField(max_length=255, required=True)
    catalog_size = fields.IntField(required=True)
    brand_pictures = fields.ListField(fields.ImageField())
    price_range = fields.IntField(required=True)
    supply_chain = fields.StringField(max_length=255, required=True)
    inventory = fields.StringField(max_length=255, required=True)
    star_rating = ConstrainedIntField(required=True)
    feedback_text = fields.StringField()
    website = fields.URLField(max_length=255, required=True, unique=True)