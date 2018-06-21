# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com

from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab
from deveops.conf import INNER_DNS,OUTER_DNS
from yodns.models import DNS
from django.db.models import Q
from dns import resolver


def reflush(obj,nameserver):
    r = resolver.Resolver()
    r.nameservers = [nameserver]
    try:
        answers = r.query(obj.recursion_name(), 'CNAME')
        for rdata in answers:
            return rdata.to_text()[:-1]
    except resolver.NoAnswer as e:
        try:
            answer = r.query(obj.recursion_name(), 'A')
            for rr in answer:
                return rr.address
        except Exception as e:
            pass
    return ''


@periodic_task(run_every=crontab(minute='*'))
def DNSFlush():
    for dns in DNS.objects.all().exclude(Q(father__isnull=True)|Q(father__father__isnull=True)):
        dns.inner_dig = reflush(dns,INNER_DNS)
        dns.dig = reflush(dns,OUTER_DNS)
        dns.save()