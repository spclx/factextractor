import date_parser as dp
import preproc

def analyze(text):
    # Разделение текста на датированные куски
    diary = dp.date_extractor_for_diary(text)

    # Очистка текста дневника
    diary = preproc.text_preproc(diary)

    # Токенизация текста дневника по предложениям
    diary['tokens'] = diary['text'].apply(lambda text: preproc.tokenizing(text))
    
    return diary