from django.contrib import admin

from debunkbot.models import (Tweet, Claim, Reply)

admin.site.register([Tweet, Claim, Reply])
