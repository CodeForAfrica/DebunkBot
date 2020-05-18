from django.contrib import admin

from debunkbot.models import Tweet, Claim

admin.site.register([Tweet, Claim])
