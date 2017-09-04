# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
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