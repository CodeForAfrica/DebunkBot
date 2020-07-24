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
    MessageTemplateSource,
    RespondListGsheet
)
from debunkbot.forms import IgnoreListGsheetForm, RespondListGsheetForm


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
        return

@admin.register(IgnoreListGsheet)
class IgnoreListGsheetAdmin(admin.ModelAdmin):
    form = IgnoreListGsheetForm

@admin.register(RespondListGsheet)
class IgnoreListGsheetAdmin(admin.ModelAdmin):
    form = RespondListGsheetForm

admin.site.register([
    Tweet,
    Claim,
    Reply,
    Impact,
    MessageTemplate,
    GoogleSheetCredentials,
    MessageTemplateSource,
])
