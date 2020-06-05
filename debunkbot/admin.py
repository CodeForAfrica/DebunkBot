from django.contrib import admin

from debunkbot.models import (
    Tweet,
    Claim,
    Reply,
    Impact,
    MessageTemplate,
    SheetInformation,
)

admin.site.register([
    Tweet,
    Claim,
    Reply,
    Impact,
    MessageTemplate,
    SheetInformation,
])
