from django.contrib import admin

from debunkbot.models import (Tweet, Claim, Reply, Impact)

admin.site.register([Tweet, Claim, Reply, Impact])
