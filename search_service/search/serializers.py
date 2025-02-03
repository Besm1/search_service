from rest_framework import serializers


class ProfileSearchSerializer(serializers.Serializer):
    profile_id = serializers.ListField(child=serializers.CharField(),required=False)
    location = serializers.ListField(child=serializers.CharField(), required=False)
    age  = serializers.ListField(child=serializers.IntegerField(), required=False)
    username = serializers.ListField(child=serializers.CharField(), required=False)
    first_name = serializers.ListField(child=serializers.CharField(), required=False)
    last_name = serializers.ListField(child=serializers.CharField(), required=False)
    tg_nick = serializers.ListField(child=serializers.CharField(), required=False)
    email = serializers.ListField(child=serializers.EmailField(), required=False)
    gender = serializers.ListField(child=serializers.CharField(), required=False)
    phone = serializers.ListField(child=serializers.CharField(), required=False)
    skill = serializers.ListField(child=serializers.CharField(), required=False)
    college = serializers.ListField(child=serializers.CharField(),required=False)
    speciality = serializers.ListField(child=serializers.CharField(), required=False)
    pers_quality = serializers.ListField(child=serializers.CharField(), required=False)
    company = serializers.ListField(child=serializers.CharField(),required=False)
    position = serializers.ListField(child=serializers.CharField(), required=False)
    specialization = serializers.ListField(child=serializers.CharField(),required=False)

    

    
    
    

