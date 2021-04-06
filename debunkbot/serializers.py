from rest_framework import serializers

from debunkbot.models import Claim, ClaimsTracker


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        exclude = ["id"]

    def get_or_create(self):
        fields = self.validated_data.copy()

        return Claim.objects.get_or_create(
            fact_checked_url=fields.pop("fact_checked_url"),
            defaults=fields,
        )


class ClaimsTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimsTracker
        exclude = ["id"]
