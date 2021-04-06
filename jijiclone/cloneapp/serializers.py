from rest_framework import serializers
from .models import Seller, Item, Transactions
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password


class SellerSerializer(serializers.ModelSerializer):
    """ Serializes our user data"""

    class Meta:
        model = Seller
        fields = '__all__'

    def validate(self, data):
        email_validation = 'email' in data and data['email']
        validate_password(password=data['password'].strip())
        errors = {}

        if not email_validation:
            errors['email'] = ['Invalid email']

        if len(errors):
            raise serializers.ValidationError(errors)

        # hash password
        data['password'] = make_password(data.get('password'))
        saved_data = {
            'firstname': data['firstname'],
            'lastname': data['lastname'],
            'email': data['email'],
            'password': data['password'],
            "is_seller": data.get("is_seller", True)
        }

        return saved_data


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'
