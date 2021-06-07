from django.contrib import admin
from account.models import Account
# from django.contrib.auth.admin import UserAdmin


# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'firstname', 'contact_number', 'last_login')
    search_fields = ('email', 'contact_number', 'firstname', 'id')
    readonly_fields = ()
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ()



admin.site.register(Account, AccountAdmin)
