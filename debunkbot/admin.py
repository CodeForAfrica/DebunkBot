from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from debunkbot.models import (
    Tweet,
    Claim,
    Reply,
    Impact,
    MessageTemplate,
    GSheetClaimsDatabase,
    GoogleSheetCredentials,
    IgnoreListGsheet,
    MessageTemplateSource
)

@admin.register(GSheetClaimsDatabase)
class GSheetClaimsDatabaseAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        # Only show deleted claims databases to superusers.
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(deleted=False)
    
    def delete_model(self, request, obj):
        # Only delete from database if the user is a superuser
        if request.user.is_superuser:
            super().delete_model(request, obj)
        else:
            obj.deleted = True
            obj.save()
        return

admin.site.register([
    Tweet,
    Claim,
    Reply,
    Impact,
    MessageTemplate,
    GoogleSheetCredentials,
    IgnoreListGsheet,
    MessageTemplateSource,
])


admin.site.unregister(User)
admin.site.unregister(Group)
