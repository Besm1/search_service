import random
import uuid
from faker import Faker
from random import randint
from datetime import datetime
from prof.models import *

def generate_fake_data(modeladmin, request, queryset):

    ProfileUseravatar.objects.all().delete()
    ProfileUserspecialization.objects.all().delete()
    ProfilePersonalquality.objects.all().delete()
    ProfileUserskill.objects.all().delete()
    ProfileEducationuser.objects.all().delete()
    ProfilePlaceofworkuser.objects.all().delete()
    ProfileProfile.objects.all().delete()
    ProfileUser.objects.all().delete()

    fake = Faker()  # Создаем объект Faker для генерации случайных данных

    # Генерация записей для ProfileProfile
    for _ in range(200):

        admin = True if random.random() <= 0.01 else False
        last_login = fake.date_time_this_decade(before_now=True, after_now=False)

        profile_profile_user = ProfileUser(
            password='12345',
            last_login=last_login, # Дата последнего логина
            is_superuser=admin,   # Админ
            username = fake.user_name(),  # Имя пользователя
            first_name=fake.first_name(),  # Имя
            last_name=fake.last_name(),  # Фамилия
            email=fake.email(),  # Электронная почта
            is_staff = True if (random.random() <= 0.05) | admin  else False,   # Персонал
            is_active = True if random.random() <= 0.95 else False,
            date_joined = fake.date_between(datetime(2020,1,1), last_login),
            id = uuid.uuid4()
        )
        profile_profile_user.save()

        profile_profile = ProfileProfile(
            id=fake.uuid4(),  # Генерируем уникальный UUID
            username=profile_profile_user.username,  # Имя пользователя
            first_name=profile_profile_user.first_name,  # Имя
            last_name=profile_profile_user.last_name,  # Фамилия
            tg_nick='@'+fake.user_name(),  # Ник в Telegram
            email=profile_profile_user.email,  # Электронная почта
            date_of_birth=fake.date_of_birth(minimum_age=18).strftime('%Y-%m-%d'),  # Дата рождения
            gender=fake.random_element(elements=['Male', 'Female']),  # Пол
            location=fake.city()[:50],  # Местоположение
            phone=fake.phone_number()[:20],  # Телефон
            token=fake.pystr(min_chars=32, max_chars=50),  # Токен
            user_id=profile_profile_user.id  # Связь с объектом ProfileUser (заменить на реальный ID)
        )
        profile_profile.save()

        # Генерация дочерних объектов
        ProfilePersonalquality.objects.create(
            quality=fake.sentence(nb_words=16, variable_nb_words=True),
            link=fake.url(),
            user=profile_profile
        )

        for child_class in  [ProfileEducationuser, ProfilePlaceofworkuser, ProfileUserskill,ProfileUserspecialization]:
            for i in range(1, randint(1, 4)):
                if child_class == ProfileEducationuser:
                    ProfileEducationuser.objects.create(
                        college=fake.company(),
                        speciality=fake.job(),
                        year_of_study=str(datetime.now().year - randint(1, 15)),
                        link=fake.url(),
                        user=profile_profile
                    )
                elif child_class == ProfileUserspecialization:
                    ProfileUserspecialization.objects.create(
                        specialization=fake.job(),
                        user=profile_profile
                    )
                elif child_class == ProfilePlaceofworkuser:
                    ProfilePlaceofworkuser.objects.create(
                        company=fake.company(),
                        position=fake.job(),
                        work_period=f"{datetime.now().year - randint(1, 10)}-{datetime.now().year}",
                        user=profile_profile
                    )
                elif child_class == ProfileUserskill:
                    ProfileUserskill.objects.create(
                        skill_name=fake.random_element([
                            # ' Языки программирования (например, Python, Java, C++)',
                            # ' Веб-разработка (HTML, CSS, JavaScript)',
                            # ' Управление базами данных (MySQL, PostgreSQL, MongoDB)',
                            # ' DevOps (Docker, Kubernetes, Jenkins)',
                            # ' Кибербезопасность (Шифрование, Анализ уязвимостей)',
                            # ' Машинное обучение (TensorFlow, Scikit-Learn)',
                            # ' Анализ данных (Pandas, NumPy, Tableau)',
                            # ' Облачные вычисления (AWS, Azure, Google Cloud)',
                            # ' Тестирование программного обеспечения (Ручное, Автоматизированное)',
                            # ' Проектирование архитектуры программного обеспечения',
                            # ' Управление проектами (Agile, Scrum)',
                            # ' Администрирование сети (TCP/IP, DNS)',
                            # ' Разработка пользовательского интерфейса (UI) и опыта взаимодействия (UX)',
                            # ' Скриптовый автопилот (Bash, PowerShell)',
                            # ' Большие данные (Hadoop, Spark)',
                            # ' Алгоритмы и структуры данных',
                            # ' Виртуализация (VMware, Hyper-V)',
                            # ' Разработка искусственного интеллекта (ИИ)',
                            # ' Интеграция систем',
                            # ' Оптимизация производительности',
                            # ' Разработка мобильных приложений (iOS, Android)',
                            # ' Техническое письмо',
                            # ' Поисковая оптимизация (SEO)',
                            # ' Безопасность кода',
                            # ' Контейнеризация (Docker, LXC)',
                            # ' Микросервисная архитектура',
                            # ' Интернет вещей (IoT) разработка',
                            # ' Хранилища данных',
                            # ' Системы управления взаимоотношениями с клиентами (CRM)',
                            # ' Разработка блокчейнов',
                            # ' Разработка и интеграция API',
                            # ' Средства бизнес-аналитики (BI)',
                            # ' Информационный поиск',
                            # ' Системы контроля версий (Git, SVN)',
                            # ' Гибкие методологии',
                            # ' Отладка и устранение неполадок',
                            # ' Обеспечение качества (QA)',
                            # ' Непрерывная интеграция / непрерывная доставка (CI/CD)',
                            # ' Обработка естественного языка (NLP)',
                            # ' Бесконечная вычислительная среда',
                            # ' Роботизированная автоматизация процессов (RPA)',
                            # ' Криптография',
                            # ' Разработка дополненной реальности (AR) и виртуальной реальности (VR)',
                            # ' Разработка видеоигр',
                            # ' Программирование встроенных систем',
                            # ' Квантовые вычисления',
                            # ' Голосовые пользовательские интерфейсы (VUIs)',
                            # ' Геопространственные технологии',
                            # ' Разработка чат-ботов',
                            # ' Цифровая криминалистика',
                            ' Python',
                            ' JavaScript',
                            ' Java',
                            ' C#',
                            ' PHP',
                            ' C++',
                            ' TypeScript',
                            ' Swift',
                            ' Kotlin',
                            ' Go (Golang)',
                            ' R',
                            ' Ruby',
                            ' Rust',
                            ' MATLAB',
                            ' Scala',
                            ' Objective-C',
                            ' Perl',
                            ' Dart',
                            ' Lua',
                            ' Julia',
                            ' Haskell',
                            ' Clojure',
                            ' Erlang',
                            ' Groovy',
                            ' COBOL',
                            ' Fortran',
                            ' Assembly',
                            ' Prolog',
                            ' Scheme',
                            ' Smalltalk'
                        ]),
                        skill_type=fake.random_element(['Hard Skill', 'Soft Skill']),
                        user=profile_profile
                    )
