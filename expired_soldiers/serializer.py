from .models import ExpiredSoldier

class ExpiredSoldierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiredSoldier
        fields = ["id", "full_name", "national_code", "father_name", "expired_file_number"]
