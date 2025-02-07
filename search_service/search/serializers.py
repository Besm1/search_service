from rest_framework import serializers


class ProfileSearchSerializer(serializers.Serializer):
    profile_id = serializers.ListField(child=serializers.CharField(),required=False
                    , help_text = "Список UUID идентификаторов профилей.")
    location = serializers.ListField(child=serializers.CharField(), required=False
                                    , help_text="Список желаемых стран/городов/регионов проживания.")
    age  = serializers.ListField(child=serializers.IntegerField(), required=False,
        help_text="Возраст (в годах). Задаётся двумя границами диапазона, верхняя может быть опущена.")
    username = serializers.ListField(child=serializers.CharField(), required=False,
        help_text="Список логинов пользователей.")
    first_name = serializers.ListField(child=serializers.CharField(), required=False,
        help_text="Список имен.")
    last_name = serializers.ListField(child=serializers.CharField(), required=False,
        help_text="Список фамилий.")
    tg_nick = serializers.ListField(child=serializers.CharField(), required=False,
        help_text="Список никнеймов в Telegram.")
    email = serializers.ListField(child=serializers.EmailField(), required=False,
        help_text="Список адресов электронной почты.")
    gender = serializers.ListField(child=serializers.CharField(), required=False,
        help_text="Пол.")
    phone = serializers.ListField(child=serializers.CharField(), required=False,
        help_text="Список номеров телефонов.")
    skill = serializers.ListField(child=serializers.CharField(), required=False,
        help_text="Список навыков. Кандидат должен обладать максимумом навыков из списка.")
    college = serializers.ListField(child=serializers.CharField(),required=False,
        help_text="Список учебных заведений.")
    speciality = serializers.ListField(child=serializers.CharField(), required=False,
        help_text="Список специальностей.")
    pers_quality = serializers.ListField(child=serializers.CharField(), required=False,
        help_text="Список личных качеств. Кандидат должен обладать максимумом личных качеств из списка."
                  " Поиск производится по \"слову целиком\".")
    company = serializers.ListField(child=serializers.CharField(),required=False,
        help_text="Список прежних/нынешнего места работы.")
    position = serializers.ListField(child=serializers.CharField(), required=False,
        help_text="Перечень возможных последних/текущих должностей.")
    specialization = serializers.ListField(child=serializers.CharField(),required=False,
        help_text="Список требуемых специализаций кандидата.")

    

    
    
    

