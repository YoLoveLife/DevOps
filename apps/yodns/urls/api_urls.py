from django.urls import path
from yodns import api as DNSAPI
urlpatterns=[
    # Resource DNS api
    path(r'v1/dns/', DNSAPI.DNSListAPI.as_view()),
    path(r'v1/dns/bypage/', DNSAPI.DNSListByPageAPI.as_view()),
    path(r'v1/dns/create/', DNSAPI.DNSCreateAPI.as_view()),
    path(r'v1/dns/<uuid:pk>/update/', DNSAPI.DNSUpdateAPI.as_view()),
    path(r'v1/dns/<uuid:pk>/delete/', DNSAPI.DNSDeleteAPI.as_view()),
]