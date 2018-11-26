# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
import uuid
import pyotp
import redis
from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import django.utils.timezone as timezone
from deveops.utils import sshkey, aes
from django.conf import settings
from authority.tasks import jumper_status_flush

__all__ = [
    "Key", "ExtendUser", "Jumper",
]

connect = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_SPACE,
    password=settings.REDIS_PASSWD,
)


def private_key_validator(key):
    if not sshkey.private_key_validator(key):
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': key},
        )


def public_key_validator(key):
    if not sshkey.public_key_validator(key):
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': key},
        )


class Key(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='')

    # 操作权限限定
    _private_key = models.TextField(max_length=4096, blank=True, null=True,
                                    validators=[private_key_validator, ])
    _public_key = models.TextField(max_length=4096, blank=True, null=True,
                                   validators=[public_key_validator, ])
    # 创建时间
    _fetch_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ('yo_list_key', u'罗列密钥'),
            ('yo_create_key', u'创建密钥'),
            ('yo_update_key', u'更新密钥'),
            ('yo_delete_key', u'删除密钥'),
        )

    @property
    def private_key(self):
        if self._private_key:
            key_str = aes.decrypt(self._private_key)
            return key_str
        else:
            return None

    @private_key.setter
    def private_key(self, private_key):
        self._private_key = aes.encrypt(private_key).decode()

    @property
    def public_key(self):
        return aes.decrypt(self._public_key)

    @public_key.setter
    def public_key(self, public_key):
        self._public_key = aes.encrypt(public_key).decode()

    @property
    def fetch_time(self):
        return self._fetch_time

    @fetch_time.setter
    def fetch_time(self, fetch_time):
        if fetch_time:
            self._fetch_time = timezone.now

    @property
    def group_name(self):
        if self.group is not None:
            return self.group.name
        else:
            return u'未指定'


class ExtendUser(AbstractUser):
    img = models.CharField(max_length=10, default='user.jpg')
    phone = models.CharField(max_length=11, default='None',)
    full_name = models.CharField(max_length=11, default='未获取')
    qrcode = models.CharField(max_length=16, default='')
    have_qrcode = models.BooleanField(default=False)
    expire = models.IntegerField(default=100)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    info = models.CharField(default='', max_length=150)

    class Meta:
        permissions = (
            ('yo_list_user', u'罗列用户'),
            ('yo_list_opsuser', u'罗列运维用户'),
            ('yo_create_user', u'新增用户'),
            ('yo_update_user', u'修改用户'),
            ('yo_delete_user', u'删除用户'),
            ('yo_list_pmngroup', u'罗列权限组'),
            ('yo_create_pmngroup', u'新增权限组'),
            ('yo_update_pmngroup', u'修改权限组'),
            ('yo_delete_pmngroup', u'删除权限组'),
            # django.contrib.auth.models.Permission django.contrib.auth.models.Group 无法重构
            ('yo_list_permission', u'罗列所有权限')
        )

    def get_8531email(self):
        return self.username + '@8531.cn'

    def get_group_name(self):
        if self.is_superuser == 1:
            return "超级管理员"
        elif self.groups.count() == 0:
            return "无权限"
        else:
            gourp_list = []
            groups = self.groups.all()
            for group in groups:
                gourp_list.append(group.name)
            if len(gourp_list) == 0:
                return ''
            else:
                return "-".join(gourp_list)

    def check_qrcode(self, verifycode):
        t = pyotp.TOTP(self.qrcode)
        print('验证器内存地址',t)
        result = t.verify(verifycode)
        return result

    @property
    def is_expire(self):
        return not connect.exists(self.username)

    @is_expire.setter
    def is_expire(self, qrcode):
        connect.set(self.username, qrcode, self.expire or 1)


class Jumper(models.Model):
    # 全局ID
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    connect_ip = models.GenericIPAddressField(default='0.0.0.0')
    # 跳板机端口
    sshport = models.IntegerField(default='52000')
    name = models.CharField(max_length=50, default="")
    info = models.CharField(max_length=200, default="", blank=True, null=True)
    _status = models.IntegerField(default=settings.STATUS_JUMPER_NO_KEY)

    class Meta:
        permissions = (
            ('yo_list_jumper', u'罗列跳板机'),
            ('yo_create_jumper', u'创建跳板机'),
            ('yo_update_jumper', u'更新跳板机'),
            ('yo_status_jumper', u'刷新跳板机器'),
            ('yo_delete_jumper', u'删除跳板机'),
        )

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self.check_status()

    def check_status(self):
        jumper_status_flush.delay(self)

    def to_yaml(self):
        return {
            u'set_fact':
                {
                    'ansible_ssh_common_args':
                        '-o ProxyCommand="ssh -p{{JUMPER_PORT}} -i {{KEY}} -W %h:%p root@{{JUMPER_IP}}"'
                }
        }


