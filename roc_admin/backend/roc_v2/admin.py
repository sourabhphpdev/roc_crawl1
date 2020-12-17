from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.utils.html import format_html
# Register your models here.


class McaInformationAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ('company_name','company_cin', 'doc_present', '_doc_info', 'other_eform_documents_present', '_other_eform_documents_information','doc_present_2020','_doc_info_2020','other_eform_documents_present_2020','_other_eform_documents_information_2020', 'timestamp_lastupdated', 'timestamp_added')
    def _doc_info(self, obj):
        print(obj.doc_information)
        if obj.doc_information:
            return format_html('<p style="white-space: nowrap;">'+obj.doc_information+'</p>' )
        return obj.doc_information
    def _other_eform_documents_information(self, obj):
        if obj.other_eform_documents_information:
            return format_html('<p style="white-space: nowrap;">'+obj.other_eform_documents_information+'</p>' )
        return obj.other_eform_documents_information

    def _doc_info_2020(self, obj):
        print(obj.doc_information)
        if obj.doc_information_2020:
            return format_html('<p style="white-space: nowrap;">'+obj.doc_information_2020+'</p>' )
        return obj.doc_information_2020
    def _other_eform_documents_information_2020(self, obj):
        if obj.other_eform_documents_information_2020:
            return format_html('<p style="white-space: nowrap;">'+obj.other_eform_documents_information_2020+'</p>' )
        return obj.other_eform_documents_information_2020


admin.site.register(McaInformation, McaInformationAdmin)

