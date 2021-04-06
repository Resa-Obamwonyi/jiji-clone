from django.db import transaction
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import Seller, Item, Transactions
from . import serializers
from .lib.lower_strip import strip_and_lower
import requests


# Signup as a Seller View
class SignUp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        with transaction.atomic():

            if not (request.data.get('firstname', '') or len(request.data.get('firstname', '') > 3)):
                return Response(
                    dict(error='Invalid Firstname, Firstname must be at least three Characters long.'),
                    status=status.HTTP_400_BAD_REQUEST)

            if not (request.data.get('lastname', '') or len(request.data.get('lastname', '') > 3)):
                return Response(
                    dict(error='Invalid Lastname, Lastname must be at least three Characters long.'),
                    status=status.HTTP_400_BAD_REQUEST)

            user_data = {
                "firstname": request.data["firstname"],
                "lastname": request.data["lastname"],
                "email": request.data["email"],
                "password": request.data["password"],
                "location": request.data["state_of_residence"]
            }
            seller_serializer = serializers.SellerSerializer(data=user_data)

            if seller_serializer.is_valid():
                seller = seller_serializer.save()
                seller.set_password(request.data["password"])

                return Response(
                    dict(success='Your account has been created successfully. Start Selling.'),
                    status=status.HTTP_201_CREATED)
            else:
                return Response(
                    seller_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


# Login View
class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = strip_and_lower(request.data.get('email', ''))
            password = request.data.get('password', '')

            if email is None or password is None:
                return Response(
                    dict(invalid_credential='Please provide both email and password'),
                    status=status.HTTP_400_BAD_REQUEST)
            try:
                db_user = User.objects.get(email=email)
            except Exception:
                return Response(
                    dict(invalid_credential='This user does not exist in our records'),
                    status=status.HTTP_400_BAD_REQUEST)

            user = check_password(password, db_user.password)

            if not user:
                return Response(
                    dict(invalid_credential='Please ensure that your email and password are correct'),
                    status=status.HTTP_400_BAD_REQUEST)

            token, _ = Token.objects.get_or_create(user=db_user)
            return Response(dict(token=token.key), status=status.HTTP_200_OK)

        except Exception as err:
            return Response(dict(error=err), status=status.HTTP_400_BAD_REQUEST)
