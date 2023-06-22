import date_parser as dp
import preproc
import category_parser as cp

def analyze(text):
    # Разделение текста на датированные куски
    diary = dp.date_extractor_for_diary(text)

    # Очистка текста дневника
    diary = preproc.text_preproc(diary)

    # Токенизация текста дневника по предложениям
    diary['tokens'] = diary['text'].apply(lambda text: preproc.tokenizing(text))
    
    # Выделение фактов из текста
    diary['loc_facts'] = diary['tokens'].apply(lambda tokens: cp.get_facts(tokens, 'locations'))
    diary['loc_words'] = diary['tokens'].apply(lambda tokens: cp.get_mentioned_words(tokens, 'locations'))

    return diary