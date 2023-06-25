import date_parser as dp
import preproc
import category_parser as cp
import sentiment_parser as sp
import streamlit as st

# def get_gender(tokens):
#     r = [token.feats['Gender'] for sent in tokenizing(text) for token in sent if (token.feats.get('Gender') and token.feats.get('Voice')) ]

# @st.experimental_memo
def analyze(text):
    # Разделение текста на датированные куски
    diary = dp.date_extractor_for_diary(text)

    # Очистка текста дневника
    diary = preproc.text_preproc(diary)

    # Токенизация текста дневника по предложениям
    diary['tokens'] = diary['text'].apply(lambda text: preproc.tokenizing(text))
    
    # # Выделение фактов из текста
    diary['loc_facts'] = diary['tokens'].apply(lambda tokens: cp.get_facts(tokens, 'locations'))
    # diary['loc_words'] = diary['tokens'].apply(lambda tokens: cp.get_mentioned_words(tokens, 'locations'))

    # Определение сентимента по записям
    # diary['sent'] = diary['tokens'].apply(lambda tokens: sp.get_overall_sentiment(tokens))
    # diary['sent_index'] = diary['sent'].apply(lambda sent: sp.get_sentiment_index(sent))

    return diary