import re

from django.db.models import Q
from prof.models import ProfileProfile, ProfileEducationuser, ProfilePersonalquality, ProfilePlaceofworkuser, \
    ProfileUserskill, ProfileUserspecialization
from .models import SearchParams
from search.utilities import calculate_age, clean_phone_number, normalize_string


class DoesNotExist(Exception):
    def __init__(self, message, extra_info):
        self.message = message
        self.extra_info = extra_info


def arrange_candidates(search_params):
    candidates = ProfileProfile.objects.all().prefetch_related(
        'profileeducationuser_set',
        'profilepersonalquality',
        'profileplaceofworkuser_set',
        'profileuserskill_set',
        'profileuserspecialization_set'
    ).distinct()        #.filter(phone__in=["001-940-715-2617x344","607-997-9715x37017"])

    weights = {}
    max_rating = 0.0

    p_properties = SearchParams.objects.filter(enabled=True)

    # Получение весов параметров
    for param, values in search_params.items():

        if not isinstance(values, list) or len(values) == 0:
            continue

        # rec = p_properties.filter(name=param).first()
        # if rec:
        #     weights[param] = rec.weight
        #     max_rating += weights[param]
        # else:
        #     weights[param] = 0
        try:
            weights[param] = p_properties.get(name=param).weight
        except SearchParams.DoesNotExist:
            print(f'В таблице SearchParams не найдено описание параметра {param}.')
            weights[param] = 0
        else:
            max_rating += weights[param]


    results = []
    if max_rating > 0:
        for candidate in candidates:
            score = calculate_candidate_rating(candidate, search_params, weights, max_rating)
            if score > 0:
                results.append((candidate.id, score))

        # Сортируем результаты по убыванию оценки
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

        return [(id_, score) for id_, score in sorted_results]
    else:
        return []

def calculate_candidate_rating(candidate_profile, search_params, weights, max_rating):
    # Инициализация переменных
    total_rating = 0.0

    # Расчет оценки по каждому параметру
    for param, values in search_params.items():
        if weights[param] == 0:
            continue
        if param == 'skill' and values:
            skills_count = (ProfileUserskill.objects.filter(user=candidate_profile)
                            .annotate(norm_skill=normalize_string('skill_name'))
                            .values_list('skill_name')
                            .distinct()
                            .filter(norm_skill__in=[v.strip().lower() for v in values])).count()
            score = float(skills_count) / len(values)
        elif param == 'pers_quality' and values:
            try:
                qualities = ProfilePersonalquality.objects.get(user=candidate_profile).quality.lower()
                matches = sum([1 if re.search(r'\b' + v.lower() + r'\b', qualities) else 0 for v in values])
                score = float(matches) / len(values)
            except Exception:
                score = 0
        elif param == 'profile_id' and values:
            score = 1 if str(candidate_profile.id) in values else 0
        elif param == 'phone' and values:
            score = 1 if clean_phone_number(candidate_profile.phone) in clean_phone_number(values) else 0
        elif param == 'age' and values:
            score = 1 if int(values[0]) < calculate_age(candidate_profile.date_of_birth) < int(values[1]) else 0
        elif param in ['location', 'username', 'first_name', 'last_name', 'tg_nick', 'email', 'gender'] and values:
            score = 1 if getattr(candidate_profile, param, None) in values else 0
        elif param in ['college', 'speciality'] and values:
            score = 1 if ProfileEducationuser.objects.filter(Q(**{f"{param}__in": values})
                                                             , user=candidate_profile).exists() else 0
        elif param in ['company', 'position'] and values:
            score = 1 if ProfilePlaceofworkuser.objects.filter(Q(**{f"{param}__in": values})
                                                                , user=candidate_profile).exists() else 0
        elif param == 'specialization' and values:
            score = 1 if ProfileUserspecialization.objects.filter(user=candidate_profile
                                                                  , specialization__in=values).exists() else 0
        else:
            score = 0

        total_rating += score * weights[param]

    return round( (100 * total_rating / max_rating) , 0)
