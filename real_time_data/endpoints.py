from authentication.http_cookie_authentication import CookieTokenAuthentication
from authentication.models import APIKey
from rest_framework import pagination, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import (AllowAny, BasePermission, IsAdminUser,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse


from .binaryreader import *
import collections
import tempfile



from instruments.base_models import InstrumentSensorPackage

from .models import RealTimeData, DecodeScript
from .serializers import (RealTimeDataSerializer, DecodeScriptSerializer)


class RealTimeDataEndpoint(viewsets.ModelViewSet):

    """
    Endpoint for CRUD on the real-time data model. This model
    is used my the AWS lambda function to control what and how
    deployments get decoded, posted to the DB, etc. 
    """

    authentication_classes = [CookieTokenAuthentication]
    queryset = RealTimeData.objects.all().order_by('-last_modified')
    serializer_class = RealTimeDataSerializer
    filterset_fields = ['active']

class DecodeScriptsEndpoint(viewsets.ModelViewSet):

    """
    Endpoint for CRUD on the decode-script model. The decode-scripts
    dynamically define Python functions which are used by the Lambda
    functions for decoding SBD binary files.  
    """

    authentication_classes = [CookieTokenAuthentication]
    queryset = DecodeScript.objects.all().order_by('-last_modified')
    serializer_class = DecodeScriptSerializer


class DecodeScriptPreviewEndpoint(viewsets.ViewSet):

    def create(self, request):
        binary_file = request.FILES.get('file')
        decode_script_id = request.data['decode_script_id']
        print(decode_script_id)

        if binary_file:
            try:
                sbd_message_bytes = BinaryReader(binary_file)
                script = DecodeScript.objects.get(id=decode_script_id)
                if not script.script:
                    return JsonResponse({'error': 'No decode script found'}, status=400)
                
                data = collections.OrderedDict()
                compiled_script = compile(script.script, "filename", "exec")
                exec(compiled_script)
                return Response({'decoded_message':data})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

    authentication_classes = [CookieTokenAuthentication]
    # queryset = DecodeScript.objects.all().order_by('-last_modified')
    # serializer_class = DecodeScriptSerializer