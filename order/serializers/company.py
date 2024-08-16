from rest_framework import serializers
from order.models import UserCompany, Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name", "logo"]

class UserCompanySerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = UserCompany
        fields = ["name", "company", "role"]
