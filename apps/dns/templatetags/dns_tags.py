# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-12-27
# Author Yo
# Email YoLoveLife@outlook.com
from django import template
from dns.models import DNS
register = template.Library()

@register.inclusion_tag("dns/tags.html")
def dns_tree():
    dns = DNS.objects.filter(father=None).get()
    return {'dns':dns.DNSson.all()}