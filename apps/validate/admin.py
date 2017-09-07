from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from models import ExtendUser
# import models
# # Register your models here.
# class ProfileInline(admin.StackedInline):
#     model = models.UserProfile
#     can_delete = False
#     verbose_name = 'userprofile'
#
# class UserAdmin(BaseUserAdmin):
#     inlines = (ProfileInline,)
#
# admin.site

admin.site.register(ExtendUser,UserAdmin)