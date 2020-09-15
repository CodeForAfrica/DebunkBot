from rest_framework import serializers

from debunkbot.models import Claim


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        exclude = ["id"]

    def get_or_create(self):
        fields = self.validated_data.copy()
        claim_first_appearance = fields.pop("claim_first_appearance")
        return Claim.objects.get_or_create(
            claim_first_appearance=claim_first_appearance, defaults=fields
        )
