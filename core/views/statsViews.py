from xml.etree.ElementTree import fromstring

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import user_passes_test
from ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.permissions import AllowAny

from core.models.statsModels import UserStatistics
from core.serializers.statsSerializers import StatsSerializer
from core.services.statsServices import UserStatisticsService
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from core.utilities.fileResponses import generate_xml_response, generate_csv_response, generate_text_response, \
    generate_json_response
from core.security.customPermissions import AdminPermission

# Get the Auth User
User = get_user_model()

# User Stats
class UserStatisticsView(APIView):
    permission_classes = [AllowAny]
    service = UserStatisticsService()
    parser_classes = [JSONParser, FormParser, MultiPartParser]  # Add the available parsers


    def get_service(self):
        model_type = self.service.determine_model_type(self.request)
        model = self.service.create_model_instance(model_type)
        return UserStatisticsService(model)

    @method_decorator(cache_page(60 * 15)) # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def get(self, request):
        fmat = request.query_params.get('format', 'json')  # Get the format from the query parameter (default: JSON)
        model = self.service.determine_model_type(request)
        user_statistics = self.service.get_all(model)
        serializer = StatsSerializer(user_statistics, many=True)

        # Return the response based on the requested format
        if fmat == 'xml':
            # Generate XML response
            xml_response = generate_xml_response(serializer.data)
            return Response(xml_response, content_type='application/xml')
        elif fmat == 'csv':
            # Generate CSV response
            csv_response = generate_csv_response(serializer.data)
            return Response(csv_response, content_type='text/csv')
        elif fmat == 'text':
            # Generate plain text response
            text_response = generate_text_response(serializer.data)
            return Response(text_response, content_type='text/plain')
        else:
            # Default: JSON response
            return Response(serializer.data)


    @method_decorator(cache_page(60 * 15)) # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def post(self, request):
        content_type = request.content_type
        model = self.service.determine_model_type(request)


        if content_type == 'text/plain':
            # Text data
            text_data = request.body.decode('utf-8')
            # Process the text data
            user_statistic = self.service.create(model, {'text_field': text_data})
            # Return a response
            return Response({'message': 'Text data processed successfully'}, status=200)

        elif content_type == 'application/json':
            # JSON data
            json_data = StatsSerializer(data=request.data)
            if json_data.is_valid():
                # Process the JSON data
                user_statistic = self.service.create(model, json_data.validated_data)
                # Return a response
                return Response({'message': 'JSON data processed successfully'}, status=200)
            else:
                return Response(json_data.errors, status=400)

        elif content_type == 'application/xml':
            # XML data
            xml_data = fromstring(request.body)
            xml_data_dict = dict(xml_data.attrib)
            xml_serializer = StatsSerializer(data=xml_data_dict)
            if xml_serializer.is_valid():
                # Process the XML data
                user_statistic = self.service.create(model, xml_serializer.validated_data)
                # Return a response
                return Response({'message': 'XML data processed successfully'}, status=200)
            else:
                return Response(xml_serializer.errors, status=400)

        elif content_type == 'text/csv':
            # CSV data
            csv_data = StatsSerializer(data=request.data)
            if csv_data.is_valid():
                # Process the CSV data
                user_statistic = self.service.create(model, csv_data.validated_data)
                # Return a response
                return Response({'message': 'CSV data processed successfully'}, status=200)
            else:
                return Response(csv_data.errors, status=400)
        else:
            return Response({'message': 'Invalid data!'}, status=400)

    @method_decorator(cache_page(60 * 15)) # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def put(self, request, statistic_id):
        model = self.service.determine_model_type(request)
        data = self.service.get_by_id(model, statistic_id)
        serializer = StatsSerializer(data=data)
        if serializer.is_valid():
            self.service.update(model, statistic_id, serializer.validated_data)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @method_decorator(cache_page(60 * 15)) # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def delete(self, request, statistic_id):
        model = self.service.determine_model_type(request)
        self.service.delete(model, statistic_id)
        return Response({'message': 'Statistic deleted successfully'}, status=200)

    # In function-based views, the dispatch process is handled implicitly by
    # the Django view system, whereas in class-based views, the dispatch
    # method explicitly handles the dispatch process.
    @method_decorator(cache_page(60 * 15)) # Cache the response for 15 minutes
    @method_decorator(ratelimit(key='user_or_ip', rate='100/h', block=True))
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        # Set the CSRF token in the response headers
        response = super().dispatch(request, *args, **kwargs)
        response['X-CSRFToken'] = get_token(request)
        return response

