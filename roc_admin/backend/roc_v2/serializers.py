from rest_framework import serializers
from .models import *

class McaInformationSerializers(serializers.Serializer):
    company_cin = serializers.CharField(max_length=255)
