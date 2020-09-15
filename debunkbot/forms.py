from django import forms

from debunkbot.models import (
    GSheetClaimsDatabase,
    IgnoreListGsheet,
    RespondListGsheet,
    WebsiteClaimDatabase,
)


class IgnoreListGsheetForm(forms.ModelForm):
    class Meta:
        model = IgnoreListGsheet
        fields = "__all__"

        help_texts = {
            "sheet_id": "The key of the Google Sheet holding the ignore list.",
            "worksheet_name": "The name of the workspace containing the ignore list",
            "column_name": "The column name containing the ignore list.",
        }


class RespondListGsheetForm(forms.ModelForm):
    class Meta:
        model = RespondListGsheet
        fields = "__all__"

        help_texts = {
            "sheet_id": "The key of the Google Sheet holding the respond to list.",
            "worksheet_name": "The name of the workspace containing the respond to accounts",
            "column_name": "The column name containing the respond to accounts.",
        }


class GSheetClaimsDatabaseForm(forms.ModelForm):
    class Meta:
        model = GSheetClaimsDatabase
        exclude = ["deleted"]


class WebsiteClaimsDatabaseForm(forms.ModelForm):
    class Meta:
        model = WebsiteClaimDatabase
        exclude = ["deleted"]
