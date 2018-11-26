# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab
from django.conf import settings
from yodns.models import DNS
from django.db.models import Q
from dns import resolver


def reflush(obj, nameserver):
    r = resolver.Resolver()
    r.nameservers = [nameserver]
    try:
        answers = r.query(obj.url, 'CNAME')
        for rdata in answers:
            return rdata.to_text()[:-1]
    except resolver.NoAnswer as e:
        try:
            answer = r.query(obj.url, 'A')
            for rr in answer:
                return rr.address
        except Exception as e:
            pass
    except resolver.NXDOMAIN as e:
        return ''
    return ''


@periodic_task(run_every=settings.YODNS_REFLUSH)
def dns_flush():
    for dns in DNS.objects.all():
        dns.internal_dig = reflush(dns, settings.INNER_DNS)
        dns.external_dig = reflush(dns, settings.OUTER_DNS)
        dns.save()
