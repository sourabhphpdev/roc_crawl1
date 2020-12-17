from django.conf import settings
from django.conf.urls import url
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'mca_info', McaInformationViews, 'mca')

for r in router.urls:
    print(r)

urlpatterns = router.urls