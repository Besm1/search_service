from rest_framework import serializers


class ProfileSearchSerializer(serializers.Serializer):
    # profile = serializers.DictField(required=False)
    location = serializers.ListField(child=serializers.CharField(), required=False)
    skills = serializers.ListField(child=serializers.CharField(), required=False)
    # education = serializers.DictField(required=False)
    # quality = serializers.ListField(child=serializers.CharField(), required=False)
    # workplace = serializers.ListField(required=False)
    # specialization = serializers.ListField(required=False)