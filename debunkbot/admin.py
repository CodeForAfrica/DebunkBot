from django.contrib import admin

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
        obj.deleted = True
        obj.save()

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
