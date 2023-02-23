from tracker.models import expenses_block
from rest_framework import serializers
class ExpensesSerializer(serializers.ModelSerializer):
    class Meta: 
        model=expenses_block
        fields='__all__'