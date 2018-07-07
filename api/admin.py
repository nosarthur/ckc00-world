from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from api.models import MyUser


@admin.register(MyUser)
class UserAdmin(DjangoUserAdmin):
    """
    Custom admin model for custom MyUser model with no email field.
    """
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff',
                                       'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name',)
    list_filter = ('is_staff',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

# We won't use Group model
admin.site.unregister(Group)
