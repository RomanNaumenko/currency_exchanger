from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Currency, CurrencyHistory
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import (CurrencySerializer,
                          CurrencyCodeSerializer,
                          CurrencyHistorySerializer,
                          CurrencyTrackingSerializer)
from django.utils import timezone
import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
class CurrentCurrencyRates(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Get current currency rates",
        responses={200: CurrencySerializer(many=True)}
    )
    def get(self, request):
        currencies = Currency.objects.all().order_by('-date_updated')
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data)


class TrackableCurrencies(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Get trackable currencies",
        responses={200: CurrencySerializer(many=True)}
    )
    def get(self, request):
        currencies = Currency.objects.filter(is_tracked=True)
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data)


class AddCurrencyForTracking(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a new currency for tracking",
        request_body=CurrencyCodeSerializer,
        responses={
            200: 'Currency {currency_code} is now being tracked',
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = CurrencyCodeSerializer(data=request.data)
        if serializer.is_valid():
            currency_code = serializer.validated_data['currency_code']
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        currency, created = Currency.objects.get_or_create(currency_code=currency_code,
                                                           defaults={"is_tracked": True})

        if not created:
            currency.is_tracked = True
            currency.save()

        return Response({'message': f'Currency {currency_code} is now being tracked'},
                        status=status.HTTP_200_OK)


class CurrencyRateHistory(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Get currency rate history for a specific period",
        manual_parameters=[
            openapi.Parameter('currency_code', openapi.IN_QUERY, description="Currency code",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date in YYYY-MM-DD",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="End date in YYYY-MM-DD",
                              type=openapi.TYPE_STRING)
        ],
        responses={200: CurrencyHistorySerializer(many=True)}
    )
    def get(self, request):
        currency_code = request.query_params.get('currency_code')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not currency_code or not start_date or not end_date:
            return Response({"error": "Missing parameters: currency_code, start_date, or end_date"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            start_date = timezone.make_aware(start_date)
            end_date = timezone.make_aware(end_date)
        except ValueError:
            return Response({"error": "Incorrect data format, should be YYYY-MM-DD"},
                            status=status.HTTP_400_BAD_REQUEST)

        history_records = CurrencyHistory.objects.filter(
            currency__currency_code=currency_code,
            date_recorded__range=(start_date, end_date)
        )

        serializer = CurrencyHistorySerializer(history_records, many=True)
        return Response(serializer.data)


class ToggleCurrencyTracking(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Toggle currency tracking",
        manual_parameters=[
            openapi.Parameter('currency_code', openapi.IN_PATH, description="Currency code", type=openapi.TYPE_INTEGER)
        ],
        request_body=CurrencyTrackingSerializer,
        responses={200: CurrencyTrackingSerializer}
    )
    def patch(self, request, currency_code):
        try:
            currency = Currency.objects.get(currency_code=currency_code)
        except Currency.DoesNotExist:
            return Response({'error': 'Currency not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CurrencyTrackingSerializer(currency, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)