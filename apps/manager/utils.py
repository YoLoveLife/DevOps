import models
def systemtype2json():
    list={}
    choices=models.Host.SYSTEM_CHOICES
    count=0
    for choice in choices:
        num=models.Host.objects.filter(systemtype=choice[0]).count()
        count+=num
        list[choice[1]]=num
    return list