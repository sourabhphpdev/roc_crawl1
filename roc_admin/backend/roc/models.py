from django.db import models
from datetime import date
from django.utils import timezone
# Create your models here.

class McaInformation(models.Model):
    company_name = models.CharField(max_length=255)
    company_cin = models.CharField(max_length=255)
    doc_present = models.BooleanField(default=False)
    doc_information = models.TextField(blank=True, null=True)
    other_eform_documents_present = models.BooleanField(default=False)
    other_eform_documents_information = models.TextField(blank=True, null=True)
    other_attachment_documents_present = models.BooleanField(default=False)
    other_attachment_documents_information = models.TextField(blank=True, null=True)
    timestamp_lastupdated = models.DateTimeField(auto_now=True)
    timestamp_added = models.DateTimeField(auto_now_add=True)
