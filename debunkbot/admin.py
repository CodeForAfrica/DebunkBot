from django.contrib import admin
from django.http import HttpResponseRedirect

from debunkbot.forms import (
    GSheetClaimsDatabaseForm,
    IgnoreListGsheetForm,
    RespondListGsheetForm,
    WebsiteClaimsDatabaseForm,
)
from debunkbot.models import (
    Claim,
    GoogleSheetCredentials,
    GSheetClaimsDatabase,
    IgnoreListGsheet,
    Impact,
    MessageTemplate,
    MessageTemplateSource,
    Reply,
    RespondListGsheet,
    ResponseMode,
    Tweet,
    WebsiteClaimDatabase,
)


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ("claim_reviewed", "claim_db")
    list_filter = ("claim_db",)


@admin.register(GSheetClaimsDatabase)
class GSheetClaimsDatabaseAdmin(admin.ModelAdmin):
    form = GSheetClaimsDatabaseForm
    list_display = ("name", "is_deleted")
    change_form_template = "debunkbot/claim_database_change_form.html"

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

    def is_deleted(self, obj):
        return obj.deleted

    def response_change(self, request, obj):
        if "restore" in request.POST:
            if request.user.is_superuser and obj.deleted:
                obj.deleted = False
                obj.save()
            self.message_user(request, "Claim Database Restored.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


@admin.register(IgnoreListGsheet)
class IgnoreListGsheetAdmin(admin.ModelAdmin):
    form = IgnoreListGsheetForm


@admin.register(RespondListGsheet)
class RespondListGsheetAdmin(admin.ModelAdmin):
    form = RespondListGsheetForm


@admin.register(WebsiteClaimDatabase)
class WebsiteClaimDatabaseAdmin(admin.ModelAdmin):
    form = WebsiteClaimsDatabaseForm


admin.site.register(
    [
        Tweet,
        Reply,
        Impact,
        MessageTemplate,
        GoogleSheetCredentials,
        MessageTemplateSource,
        ResponseMode,
    ]
)

admin.site.site_header = "DebunkBot Admin"
admin.site.site_title = "DebunkBot Admin Portal"
