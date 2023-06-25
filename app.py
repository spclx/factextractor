import streamlit as st
import diary as d
import sentiment_parser as sp
import network_builder as nb
from pyvis.network import Network
import streamlit.components.v1 as components
import word_transformations as wt

st.title('Автоматический аннотатор')

# st.markdown("Скопируйте текст дневика в это поле или выберите для теста один из подготовленных отрывков.")

txt = st.text_area('Скопируйте текст дневика в это поле', height=100)

option = st.selectbox(
    'Или выберите один из тестовых текстов дневников:',
    ('Выбрать...', 'Анатолий Василивицкий', 'Мария Германова'))

if option == 'Анатолий Василивицкий':
    with open('test_1.txt', 'r') as f:
        txt = f.read()
elif option == 'Мария Германова':
    with open('test.txt', 'r') as f:
        txt = f.read()


# diary = st.text_area('Текст дневника')
if st.button('Обработать') and txt != '':
    df = d.analyze(txt)
    # st.dataframe(df)
    # for_chart = sp.data_for_sentiment_chart(df).set_index('n_date')
    # st.markdown('### График сентимента по записям дневника (тест)')
    # st.line_chart(data=for_chart)
    # st.experimental_memo.clear()
    graph = nb.build_graph(df)

    GENDER = wt.get_gender(df['tokens'])

    st.markdown(f'**Аннотация этого дневника:** {nb.annotation(graph, GENDER)}')

    textnet = Network( height='400px',
                       width='100%',
                       bgcolor='white',
                       font_color='black'
                      )
    
    textnet.from_nx(graph)

    textnet.repulsion(
                        node_distance=420,
                        central_gravity=0.33,
                        spring_length=110,
                        spring_strength=0.10,
                        damping=0.95
                       )
    
    try:
        path = '/tmp'
        textnet.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    except:
        path = '/html_files'
        textnet.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    components.html(HtmlFile.read(), height=435)

# if st.button('Обработать'):
#     df = d.analyze(diary)
#     st.dataframe(df)
#     for_chart = sp.data_for_sentiment_chart(df).set_index('n_date')
#     st.markdown('### График сентимента по записям дневника (тест)')
#     st.line_chart(data=for_chart)

