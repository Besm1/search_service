from datetime import datetime
from django.db.models import Func

# Функция для удаления пробелов и приведения к нижнему регистру
def normalize_string(string):
    return Func(Func(string, function='TRIM'), function='LOWER')


def calculate_age(birth_date_str):
    # Преобразуем строку в объект datetime.date
    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
    today = datetime.now().date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def clean_phone_number(pn) -> str:
    """
    Форматирует ("очищает") телефонный номер (или список номеров) для сравнения номеров:
    - оставляет только цифры.
    - в списке номеров знак "+" и разделители ',:;+\n' преобразует в '|'.
    - в начало и в конец строки добавляет по одному разделителю, если только там их нет.
    Таким образом можно достаточно точно определить, входит ли очищенный телефонный номер в очищенный список номеров.
    :param pn:
    :return:
    """
    def  clean_phone_str(pn:str) -> str:
        pn = ''.join([ch if ch.isdigit() else ('|' if ch in ',:;+\n' else '') for ch in pn ])
        return pn.strip('|') if pn else ''


    if isinstance(pn, str):
        return '|' + clean_phone_str(pn) + '|'
    elif isinstance(pn, (list, set)):
        return ''.join('|'+clean_phone_str(p_) for p_ in pn) + '|'


if __name__ == '__main__':
    print(clean_phone_number('+7(916)688-48-97'))
    print(clean_phone_number('+7(916)688-48-97, +7(916)851-50-14'))
    print(clean_phone_number(['+7(916)688-48-97', '+7(916)851-50-14']))

