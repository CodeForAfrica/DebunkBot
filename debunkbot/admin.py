from django.contrib import admin
from django.http import HttpResponseRedirect

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
    RespondListGsheet,
    ResponseMode
)
from debunkbot.forms import IgnoreListGsheetForm, RespondListGsheetForm, GSheetClaimsDatabaseForm


@admin.register(GSheetClaimsDatabase)
class GSheetClaimsDatabaseAdmin(admin.ModelAdmin):
    form = GSheetClaimsDatabaseForm
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
    
    def response_change(self, request, obj):
        if "restore" in request.POST:
            obj.deleted = False
            obj.save()
            self.message_user(request, "Claim Database Restored.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

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
    ResponseMode
])

admin.site.site_header = "Debunk bot Admin"
admin.site.site_title = "Debunk bot Admin Portal"
