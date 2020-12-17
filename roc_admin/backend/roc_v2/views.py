# from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.request import Request
from django.core import serializers as serial
import json

class McaInformationViews(viewsets.ViewSet):
    # queryset = McaInformation.objects.all()
    serializer_class = McaInformationSerializers

    @action(methods=['get'], detail=False)
    def cinList(self, request):
        query = McaInformation.objects.values_list('company_cin', flat=True)
        res = json.dumps(list(query))
        return Response(res)

    @action(methods=['post'], detail=False)
    def cinMarked(self, request):
        post_data = request.data
        print(post_data['cinNumer'])
        obj = McaInformation.objects.get(company_cin =post_data['cinNumer'] )
        if obj:
            obj.doc_present = post_data['doc_present'] if 'doc_present' in post_data.keys() else obj.doc_present
            obj.doc_information = post_data['doc_information'] if 'doc_information' in post_data.keys() else obj.doc_information
            obj.other_eform_documents_present = post_data['other_eform_documents_present'] if 'other_eform_documents_present' in post_data.keys() else obj.other_eform_documents_present
            obj.other_eform_documents_information = post_data['other_eform_documents_information'] if 'other_eform_documents_information' in post_data.keys() else obj.other_eform_documents_information
            obj.doc_present_2020 = post_data['doc_present_2020'] if 'doc_present_2020' in post_data.keys() else obj.doc_present_2020
            obj.doc_information_2020 = post_data['doc_information_2020'] if 'doc_information_2020' in post_data.keys() else obj.doc_information_2020
            obj.other_eform_documents_present_2020 = post_data['other_eform_documents_present_2020'] if 'other_eform_documents_present_2020' in post_data.keys() else obj.other_eform_documents_present_2020
            obj.other_eform_documents_information_2020 = post_data['other_eform_documents_information_2020'] if 'other_eform_documents_information_2020' in post_data.keys() else obj.other_eform_documents_information_2020
            obj.save()
            return Response('success',status=200)
        else:
            return Response('Not have cin', status=404)


