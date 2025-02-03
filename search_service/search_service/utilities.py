from django.db import models

from django.db.models import Func, F, Value
from django.db.models.functions import Cast
from datetime import datetime


def calculate_age(birth_date_str):
    # Преобразуем строку в объект datetime.date
    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()

    today = datetime.now().date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    return age


class NormalizePhoneNumbers(Func):
    function = 'ARRAY'
    template = '%(function)s(SELECT %(function)s(%(expressions)s))'

    def __init__(self, expression, **extra):
        super().__init__(expression, **extra)

    def as_sql(self, compiler, connection):
        sql_parts = []
        params = []
        for expr in self.source_expressions:
            sql, param = compiler.compile(expr)
            sql_parts.append(sql)
            params.extend(param)

        placeholder = '%s' if connection.features.use_returning_into else '%s::TEXT[]'
        return placeholder % ', '.join(sql_parts), params

def clean_phone_number(pn:str) -> str:
    '''
    Форматирует ("очищает") телефонный номер (или список номеров) для сравнения номеров:
    - оставляет только цифры.
    - в списке номеров знак "+" и все возможные разделители преобразует в '|'.
    - в начало и в конец строки добавляет по одному разделителю, если только там их нет.
    Таким образом можно достаточно точно определить, входит ли очищенный телефонный номер в очищенный список номеров.
    :param pn:
    :return:
    '''
    pn = ''.join([ch if ch.isdigit() else ('|' if ch in ',:;+\n' else '') for ch in pn ])
    if  pn:
        pn = '|' + pn.strip('|') + '|'
    return pn


# if __name__ == '__main__':
#     print(clean_phone_number('79166884897') in clean_phone_number('+7(916) 688-48-97,+7(916)851-5014'))