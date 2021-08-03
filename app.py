import streamlit as st 
from multiapp import MultiApp
from Apps import home
from Apps.Streamlit_Spotify import spotify
from Apps.Streamlit_recomendacao import recomendacoes
from Apps.Streamlit_reconhecimento_rostos import reconhecimento
from Apps.Streamlit_bolsa_2021 import market



app = MultiApp()

st.set_page_config(layout = 'wide')

st.title("Pedro Dellazzari - Portfólio")

app.add_app("Home", home.app)
app.add_app("Spotify Analyses", spotify.app)
app.add_app("Recomendações de filmes", recomendacoes.app)
app.add_app("Reconhecimento de faces em imagens", reconhecimento.app)
app.add_app("Monitoramento Bolsa de Valores CNN", market.app)


app.run()