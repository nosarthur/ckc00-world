from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from api.models import MyUser, Tag, Division


@admin.register(MyUser)
class UserAdmin(DjangoUserAdmin):
    """
    Custom admin model for custom MyUser model with no email field.
    """
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields':
            ('first_name', 'last_name', 'homepage', 'employer', 'gender',
             'division', 'tags', 'city')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff',
                                       'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': ('email', 'first_name', 'last_name', 'gender', 'homepage',
            'employer', 'city',
                       'password1', 'password2'),
        }),
    )
    list_display = ('last_name', 'first_name', 'email', 'get_division', 'city')
    list_filter = ('is_staff', 'is_superuser', )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('last_name', 'first_name',)

    def get_division(self, obj):
        if obj.division:
            return obj.division.name + obj.division.number
        return None

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ['name', 'number']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_users']

    def get_users(self, obj):
        users = obj.myuser_set.all()
        return [u.get_full_name() for u in users]


# We won't use Group model
admin.site.unregister(Group)
