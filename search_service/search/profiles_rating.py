from django.db.models import Q, F
from prof.models import ProfileProfile, ProfileEducationuser, ProfilePersonalquality, ProfilePlaceofworkuser, \
    ProfileUserskill, ProfileUserspecialization
from .models import SearchParams
from search.utilities import calculate_age, clean_phone_number, normalize_string


def calculate_candidate_score(candidate_profile, search_params):
    # Инициализация переменных
    total_rate = 0.0
    weights = {}

    # Получение весов параметров
    for param, values in search_params.items():
        if not isinstance(values, list) or len(values) == 0:
            continue

        try:
            weights[param] = SearchParams.objects.get(name=param).weight
        except SearchParams.DoesNotExist:
            weights[param] = 1.0

    # Расчет оценки по каждому параметру
    for param, values in search_params.items():
        if param == 'skill' and values:
            skills_count = (ProfileUserskill.objects.filter(user=candidate_profile)
                            .annotate(norm_skill=normalize_string('skill_name'))
                            .values_list('skill_name')
                            .distinct()
                            .filter(norm_skill__in=[v.strip().lower() for v in values])).count()
            score = float(skills_count) / len(values)
        elif param == 'pers_quality' and values:
            qualities = ProfilePersonalquality.objects.filter(user=candidate_profile)
            matches = sum([1 for q in qualities if any(v in q.quality.lower() for v in values)])
            score = float(matches) / len(values)
        elif param == 'profile_id' and values:
            score = 1 if getattr(candidate_profile, 'id', None) in values else 0
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

        total_rate += score * weights[param]

    return total_rate

def arrange_candidates(search_params):
    candidates = ProfileProfile.objects.all().prefetch_related(
        'profileeducationuser_set',
        'profilepersonalquality',
        'profileplaceofworkuser_set',
        'profileuserskill_set',
        'profileuserspecialization_set'
    ).distinct()        #.filter(phone__in=["001-940-715-2617x344","607-997-9715x37017"])

    results = []
    for candidate in candidates:
        score = calculate_candidate_score(candidate, search_params)
        if score > 0:
            results.append((candidate.id, score))

    # Сортируем результаты по убыванию оценки
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

    return [(id_, score) for id_, score in sorted_results]
