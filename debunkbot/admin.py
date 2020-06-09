from django.contrib import admin

from debunkbot.models import (
    Tweet,
    Claim,
    Reply,
    Impact,
    MessageTemplate,
    GSheetClaimsDatabase,
    DebunkBotGsheet,
)

admin.site.register([
    Tweet,
    Claim,
    Reply,
    Impact,
    MessageTemplate,
    GSheetClaimsDatabase,
    DebunkBotGsheet,
])
