import streamlit as st
import diary as d
import sentiment_parser as sp
# import altair as alt

st.title('Автоматический аннотатор')

st.markdown("Скопируйте текст дневика в это поле или выберите для теста один из подготовленных отрывков.")

with open('test.txt', 'r') as f:
    TEST = f.read()
# diary = st.text_area('Текст дневника')
if st.button('Быстрая обработка на тестовом тексте '):
    df = d.analyze(TEST)
    st.dataframe(df)
    for_chart = sp.data_for_sentiment_chart(df).set_index('n_date')
    st.markdown('### График сентимента по записям дневника (тест)')
    st.line_chart(data=for_chart)

# if st.button('Обработать'):
#     df = d.analyze(diary)
#     st.dataframe(df)
#     for_chart = sp.data_for_sentiment_chart(df).set_index('n_date')
#     st.markdown('### График сентимента по записям дневника (тест)')
#     st.line_chart(data=for_chart)

