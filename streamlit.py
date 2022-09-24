# coding: utf-8

from pydoc import describe
import streamlit as st
from PIL import Image
import altair as alt

from app import sc


st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)


st.image(Image.open(r'.streamlit/logo_citadel.png'))


st.markdown(
    """
    
    CITADEL SUMMER SCHOOL 2022 -
    THEME: ANALYSE DE LA SITUATION SECURITAURE DU BURKINA FASO AVEC L'IA
   
    """
)

# sidebar
st.sidebar.header('Features')
feature = st.sidebar.selectbox(
    'select feature',
    ['describe dataset', 'show dataset distribution', 'explore dataset']
)



def description():
    st.markdown(
        """
        #### Description
        """
    )
    describe = list(sc.describe_dataset().items())
    col1, col2, col3 = st.columns(3)
    col1.metric(describe[0][0], describe[0][1])
    col2.metric(describe[1][0], describe[1][1])
    col3.metric(describe[2][0], describe[2][1])

    col1, col2, col3 = st.columns(3)
    col1.metric(describe[3][0], describe[3][1])
    col2.metric(describe[4][0], describe[4][1])
    col3.metric(describe[5][0], describe[5][1])

def comments_distribution():
    st.markdown(
        """
        #### Distribution des commentaires par article
        """
    )

    # distrubtion
    source = sc.get_dataset()['comments_number']
    st.bar_chart(source)


def explore_dataset():                 
    # show json
    st.markdown(
        """
        #### Visualisation contenu
        """
    )
    samples = sc.get_samples()
    articles = {}
    i = 0
    for sample in samples:
        i = i + 1
        title = sample['article_title']
        key = f'{i} - {title}'
        value = sample
        articles[key] = value

    article_select = st.selectbox(
        'choisir un article',
        list(articles.keys())
    )
    st.json(articles.get(article_select))


#### RUN
call = {
    'describe dataset': description,
    'show dataset distribution': comments_distribution,
    'explore dataset': explore_dataset,
}

call.get(feature)()

