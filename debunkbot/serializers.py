from rest_framework import serializers

from debunkbot.models import Claim


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        exclude = ["id"]
