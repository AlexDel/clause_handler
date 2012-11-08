# coding=utf-8
import english_handler, russian_handler, normalizer

def split_to_clauses(sentence = '', language=''):

    """
    метод разбивает предложение на клаузы,
    выбирая по языку нужные обработчики
    """
    if language == 'ru':
        return russian_handler.process(sentence)

    elif language == 'en':
        return english_handler.process(sentence)

    else:
        return ''


def check_stream(stream_a, stream_b):
    """
    метод осуществояет проверку, и возвращает код ошибки
    """

    response = {'code':0,'description':'Unknown error'}

    if len(stream_a) == 1 and len(stream_b) == 1:
        response['code'] = 2
        response['description'] = 'No clauses for matching found'


    elif len(stream_a) != len(stream_b):
        response['code'] = 3
        response['description'] = "Clauses' size don't match"

    elif stream_b['type'] != stream_a['type']:
        response['code'] = 4
        response['description'] = "Types of clauses' don't match"

    elif stream_a[type]  == 'subord' and (stream_b['tense'] == 'past' or stream_a['tense'] == 'past'):
        response['code'] = 5
        response['description'] = "Main clause contain past tense."

    elif len(stream_a) == len(stream_b):
        response['code'] = 1
        response['description'] = 'Clauses are found and ready to be matched'

    return response


def merge_clauses(sent1, sent2):
    #TODO - здесь будет функция обмена с  другими приложением. допишется после консультации с Гошей

    return True


