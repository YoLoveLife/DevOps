import models
import json
def systemtypeQuery():
    list=[]
    choices=models.Host.SYSTEM_CHOICES
    count=0
    for choice in choices:
        dit={}
        dit['name']=choice[1]
        dit['value']=models.Host.objects.filter(systemtype=choice[0]).count()
        list.append(dit)
    return json.dumps(list, ensure_ascii=False, encoding='UTF-8')

def groupQuery():
    list=[]
    grouplist=models.Group.objects.all()
    for group in grouplist:
        dit={}
        dit['name']=group.name
        dit['value']=group.hosts.count()
        list.append(dit)
    return json.dumps(list, ensure_ascii=False, encoding='UTF-8')