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

    elif len(stream_a) == len(stream_b):
        response['code'] = 1
        response['description'] = 'Clauses are found and ready to be matched'

    elif len(stream_a) != len(stream_b):
        response['code'] = 3
        response['description'] = "Clauses' size don't match"

    return response


def merge_clauses(sent):
    return True

