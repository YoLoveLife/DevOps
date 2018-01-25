import models
import json
from django.db.models import Q

def deployQuery(users):
    list=[]
    for user in users.all():
        dit={}
        dit['name'] = user.last_name
        dit['value'] = models.XMT.objects.filter(user=user,status=1).count()
        list.append(dit)
    print(list)
    return json.dumps(list, ensure_ascii=False, encoding='UTF-8')
