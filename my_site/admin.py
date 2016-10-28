from django.contrib import admin

from my_site.models import Client, User, Property, Meeting


class PropertyInline(admin.TabularInline):
    model = Property
    extra = 0


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email',)
    list_filter = ['username', 'email', ]
    search_fields = ['username', 'email', ]
    # list_editable = ('email',)
    inlines = [PropertyInline, ]
    list_per_page = 20
    exclude = ("password",)
    # readonly_fields = ("password",)


class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 0


class ClientAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'phone',)
    inlines = [MeetingInline, ]


admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
