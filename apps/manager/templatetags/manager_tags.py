from django import template
from django.utils import timezone
from django.conf import settings
register = template.Library()

@register.inclusion_tag("dns/tags.html")
def dns_tree():
    dns = DNS.objects.filter(father=None).get()
    return {'dns':dns.DNSson.all()}