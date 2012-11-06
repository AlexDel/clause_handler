# coding=utf-8

def normalize(clause):
    #убираем лишние пробелы с боков
    """
    этот модуль нормализует и причесывает предложения до канонического вида

    """
    clause = clause.strip()

    clause = unicode(clause)

    #убираем лишние знаки препинанияв в конце
    if clause.endswith((u',',u';',u'-',u':',u'/',u'.')):
        clause = clause[:-1]

    #делаем заглавную букву в начале и точку в конце
    clause = clause[0].upper() + clause[1:] + u'.'

    return clause