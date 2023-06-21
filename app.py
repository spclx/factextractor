import streamlit as st
import diary as d

st.title('Автоматический аннотатор')

st.markdown("Скопируйте текст дневика в это поле или выберите для теста один из подготовленных отрывков.")

diary = st.text_area('Текст дневника')

if st.button('Обработать'):
    st.dataframe(d.analyze(diary))
