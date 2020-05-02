from mongoengine import *
from datetime import datetime

connect(
    db="bar",
    host="localhost",
    port=27017
)

class Product (EmbeddedDocument):
    sku = IntField(required=True, unique=True)
    name = StringField(required=False)
    description = StringField(required=True)
    qty = IntField(required=False, default=0 )
    price = FloatField(required=False, default=0.0)
    updated_at = datetime.utcnow()

class Member (EmbeddedDocument):
    client_id = IntField(required=True, min_value=1)
    name = StringField(required=True, unique=True)
    email = StringField(required=True)
    password = StringField(required=True)
    created_at = datetime.utcnow()

class Order (EmbeddedDocument):
    order_id = IntField(required=True, min_value=1)
    client_id = IntField(required=True)
    updated_at = DateTimeField(required=False, default=datetime.utcnow)
    products = ListField(Product)