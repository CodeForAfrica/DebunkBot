from rest_framework import serializers

from debunkbot.models import Claim, ClaimsDatabase


class ClaimSerializer(serializers.ModelSerializer):
    claim_db_name = serializers.CharField()

    class Meta:
        model = Claim
        exclude = ["id"]

    def validate_claim_db_name(self, value):
        # Ensure the claim Db exists
        claim_db = ClaimsDatabase.objects.filter(name=value).first()
        if not claim_db:
            raise serializers.ValidationError("No such claim database")
        return value

    def create(self, validated_data):
        claim_db_name = validated_data.pop("claim_db_name")
        claim_db = ClaimsDatabase.objects.get(name=claim_db_name)
        claim = Claim.objects.create(**validated_data, claim_db=claim_db)
        return claim
