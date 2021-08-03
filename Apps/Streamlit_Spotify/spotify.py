#Importando as bibliotecas
#Importando as bibliotecas 
import pandas as pd 
import matplotlib.pyplot as plt
import numpy 
import requests
import base64
import json
import plotly.express as px
import streamlit as st 

tracks_name = []
tracks_artist = []
tracks_album = []
tracks_ms = []
tracks_added_date = []
tracks_release_date = [] 
play_name = []

#Criando a função para chamar a página 
def app():

    #Criando a função para pegar o código token para acessar a API 
    def token():

        #Client id e secret 
        client_id = 'f458fe65aad84c498981d32b46d9d84e'
        client_secret = '3bfaa00a54d44bae96e1810d90808363'

        #Criando a lista de credenciais 
        client_creds = f"{client_id}:{client_secret}"

        #Fazendo o encoding das credenciais para 64 
        client_creds_b64 = base64.b64encode(client_creds.encode())

        #Criando os parâmetros 
        token_url = 'https://accounts.spotify.com/api/token'
        method = "POST"
        token_data = {'grant_type': "client_credentials"}
        token_header = {"Authorization" : f"Basic {client_creds_b64.decode()}"}

        #Fazendo o post para recuperar o json com o token
        response = requests.post(token_url, data=token_data, headers=token_header)

        #Pegando o json 
        token_response = response.json()

        #Pegando o token de acesso 
        access_token = token_response['access_token']

        return access_token

    #Criando a função para pegar as playlists do usuário 
    def search_playlist(userid):

        #Pegando o endpoint do usuário 
        playlist_url_call = "https://api.spotify.com/v1/users/{}/playlists".format(userid)

        #Criando a url inteira 
        playlist_url_full = requests.get(playlist_url_call, headers={'Authorization':'Bearer ' + token()})

        #Pegando o json 
        playlists = playlist_url_full.json()

        #Pegando os nomes das playlists
        names = []
        i = 0 
        for items in playlists['items']:
            names.append(playlists['items'][i]['name'])
            i = i + 1

        #Pegando o total de músicas dentro de uma playlist 
        tracks = []
        i = 0 
        for items in playlists['items']:
            tracks.append(playlists['items'][i]['tracks']['total'])
            i = i + 1

        #Pegando o id de cada playlist 
        playlist_id = []
        i = 0 
        for items in playlists['items']:
            playlist_id.append(playlists['items'][i]['id'])
            i = i + 1

        #Criando o dataframe 
        playlist_df = pd.DataFrame()

        #Colocando os valores no dataframe
        playlist_df['Name'] = names
        playlist_df['Tracks'] = tracks
        playlist_df['ID'] = playlist_id

        #Retornando o dataframe
        return playlist_df

    #Criando a função para pegar todas as músicas dentro da playlist 
    def search_tracks(playlistid):
        global tracks_name 
        global tracks_artist 
        global tracks_album
        global tracks_ms
        global tracks_added_date
        global tracks_release_date 
        global play_name 

        #Criando a url da playlist 
        playlists_tracks_url = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlistid)

        #Pegando o json 
        tracks_get_data = requests.get(playlists_tracks_url, headers={'Authorization':'Bearer ' + token()})

        #Criando o json 
        tracks_json = tracks_get_data.json()

        #Pegando o nome das músicas 
        i = 0 
        for items in tracks_json['items']:
            try:
                tracks_name.append(tracks_json['items'][i]['track']['name'])
                i = i + 1
            except:
                i = i + 1 

        #Pegando o autor da múscia 
        i = 0 
        for items in tracks_json['items']:
            try:
                tracks_artist.append(tracks_json['items'][i]['track']['artists'][0]['name'])
                i = i + 1
            except:
                i = i + 1 

        #Pegando o nome do álbum 
        i = 0 
        for items in tracks_json['items']:
            try:
                tracks_album.append(tracks_json['items'][i]['track']['album']['name'])
                i = i + 1 
            except:
                i = i + 1

        #Pegando o ms da música 
        i = 0 
        for items in tracks_json['items']:
            try:
                tracks_ms.append(tracks_json['items'][i]['track']['duration_ms'])
                i = i + 1 
            except:
                i = i + 1 

        #Pegando o dia em que a música foi adicionada na playlist 
        i = 0 
        for items in tracks_json['items']:
            try:
                tracks_added_date.append(tracks_json['items'][i]['added_at'])
                i = i + 1
            except:
                i = i + 1 

        #Pegando o lançamento da música
        i = 0 
        for items in tracks_json['items']:
            try:
                tracks_release_date.append(tracks_json['items'][i]['track']['albm']['release_date'])
                i = i + 1 
            except:
                tracks_release_date.append("0")
                i = i + 1

        #Pegando o nome das playlist em questão 
        for i in tracks_json['items']:
            play_name.append(dataframe_playlist['Name'][dataframe_playlist['ID']==playlistid].item())


        #Dentro do spotify há algumas playlists que tem erros nas primeiras músicas
        #Então usar a condicional para eliminar esses erros caso ocorram
        if len(tracks_added_date) - len(tracks_name) != 0:
            elems = len(tracks_added_date) - len(tracks_name)

            #Arrumando os valores
            tracks_added_date = tracks_added_date[elems:]
            play_name = play_name[elems:]
            tracks_release_date = tracks_release_date[elems:]            


    #APLICATIVO

    #Criando o título 
    st.header("Análise de Playlist do Spotify")

    st.markdown("Essa ferramenta tem como objetivo entregar insights sobre as playlists públicas dos usuários dentro do aplicatio 'Spotify'\n\nVERSÃO - 0.1")

    #Criando as caixas de expansão 
    #Explicando como a ferramenta funciona
    how = st.beta_expander("Como funciona?")
    how.markdown("A ferramenta utiliza a API pública para desenvolvedores do próprio Spotify, ou seja, todos os recursos utilizados nessa ferramenta são providos pelo próprio aplicativo")

    #Mostrando como pegar nome de usuário
    user_name = st.beta_expander("Como pegar meu código de usuário")
    user_name.markdown("Para pegar seu código de usuário é necessário seguir as seguintes etapas\n\n1-Clique na sua foto no canto superior direito dentro do aplicativo\n\n2-Clique em conta\n\n3-Copie e cole o código de usuário para utilizar a ferramenta")

    #Perguntas frequentes
    faq = st.beta_expander("FAQ")
    faq.markdown("- A API apenas traz informações das playlists públicas do perfil\n\n- Nenhuma informação ficará armazenada após o uso da ferramenta\n\n")

    #Melhorias dentro do código
    improv = st.beta_expander("Sabe como melhorar esse código?/Sugestões?")
    improv.markdown("Caso tenha alguma sugestão para melhorar o código fique à vontade para entrar em contato pelo [LinkedIn](https://www.linkedin.com/in/pedrodellazzari/)")

    #Créditos da aplicação
    creditos = st.beta_expander("Créditos")
    creditos.markdown("Pedro Dellazzari\n\nE-mail: pedrocdellazzari@gmail.com\n\n[LinkedIn](https://www.linkedin.com/in/pedrodellazzari/)")

    #Criando o side widget 
    st.sidebar.title("Parâmetro de busca")

    #Descrição
    user_id = st.sidebar.text_input("Coloque aqui o seu código de usuário")
    st.sidebar.markdown("Caso não saiba como procurar seu código de usuário veja as caixas de seleção ao lado")

    #Criando o botão
    button = st.sidebar.button("Analisar minhas playlists")

    if button:
        #Criando o dataframe de playlist
        dataframe_playlist = search_playlist(user_id)

        #Pegando as músicas dentro de cada playlist 
        for item in dataframe_playlist['ID']:
            search_tracks(item)

        #Criando os valores com as músicas dentro da playlist 
        dataframe_tracks = pd.DataFrame()
        dataframe_tracks['Added'] = tracks_added_date
        dataframe_tracks['Release'] = tracks_release_date
        dataframe_tracks['Name'] = tracks_name
        dataframe_tracks['Artist'] = tracks_artist        
        dataframe_tracks['Album'] = tracks_album
        dataframe_tracks['Ms'] = tracks_ms                
        dataframe_tracks['Playlist'] = play_name

        #Arrumando o campo de data 
        dataframe_tracks['Added'] = dataframe_tracks['Added'].str.replace("T"," ")
        dataframe_tracks['Added'] = dataframe_tracks['Added'].str.replace("Z"," ")

        #Transformando a coluna de Added em data 
        dataframe_tracks['Added'] = pd.to_datetime(dataframe_tracks['Added'])

        #Pegando o dia da semana | hora | data separado entre as colunas 
        dataframe_tracks['Week'] = dataframe_tracks['Added'].dt.dayofweek + 1
        dataframe_tracks['Hour'] = dataframe_tracks['Added'].dt.hour
        dataframe_tracks['Added'] = dataframe_tracks['Added'].dt.date  

        #Colocando os títulos das pesquisas 
        st.markdown("<h1 style='text-align:center'>Veja o resultado</h1>", unsafe_allow_html=True)

        #---------------------- GROUPBY -----------------

        #Groupby das músicas adicionadas por data 
        tracks_per_date = dataframe_tracks.groupby(['Added','Playlist'])['Name'].count().reset_index().sort_values(by='Added')

        #Group by por dia da semana 
        tracks_per_dayweek_and_hour = dataframe_tracks.groupby(['Week','Hour'])['Name'].count().reset_index()

        #Group by por artista 
        tracks_per_artists = dataframe_tracks.groupby(['Artist'])['Name'].count().reset_index().sort_values(by='Name', ascending=False)


        #---------------------- GRAFICOS -----------------
        #GRÁFICO - Playlists com mais músicas 
        bar_playlists = px.bar(dataframe_playlist.sort_values(by='Tracks', ascending=False).head(6), x='Name',y='Tracks', text='Tracks', color_discrete_sequence=['#1DB954'], width=500)
        bar_playlists.update_xaxes(showline=True, mirror=True, linecolor='black', linewidth=2, tickangle=25)
        bar_playlists.update_yaxes(showline=True, mirror=True, linecolor='black', linewidth=2)
        bar_playlists.update_layout(title_text='Músicas adicionadas por playlists', title_x=0.5)

        #GRÁFICO - Porcentagem de músicas adicionadas por playlists 
        pie_playlists = px.pie(dataframe_playlist.head(6), values='Tracks', names='Name', title="Porcentagem de músicas por Playlists", width=500)
        pie_playlists.update_layout(title_x=0.5)

        #GRÁFICO - Músicas adicionadas por tempo 
        tracks_added_trhou_time = px.line(tracks_per_date, x='Added', y='Name', color='Playlist', title="Músicas adicionadas por data e playlists", width=1000)
        tracks_added_trhou_time.update_layout(title_x=0.5)

        #GRÁFICO - Músicas adicionadas por dia da semana 
        tracks_added_weekday = px.density_heatmap(tracks_per_dayweek_and_hour, x='Week', y='Hour', nbinsy=10, color_continuous_scale='tealgrn', title="Músicas adicionadas por semana e hora", width=600)
        tracks_added_weekday.update_layout(title_x=0.5)

        #GRÁFICO - Músicas adicionadas por artistas procentagem pie
        bar_artists = px.pie(tracks_per_artists.head(5), values='Name', names='Artist', title="Maior artista em todas as playlists", width=500)
        bar_playlists.update_layout(title_x=0.5)
        
        #GRÁFICO - Músicas adicionadas por artistas barras (maiores)
        pie_artists = px.bar(tracks_per_artists.head(10), x='Artist', y='Name', title='Artistas mais adicionados', color_discrete_sequence=["#1db954"], width=500)
        pie_playlists.update_layout(title_x=0.5)
        
        #Criando as colunas
        col1,col2 = st.beta_columns(2)

        #Colocando os gráficos no layout certo 
        col1.plotly_chart(pie_playlists, use_column_width=True)
        col2.plotly_chart(bar_playlists, use_column_width=True)

        #Colocando o gráfico inteiro 
        st.plotly_chart(tracks_added_trhou_time)

        #Colocando os gráficos no layout certo 
        col3, col4 = st.beta_columns(2)

        #Colocando os gráficos no layout certo 
        col3.plotly_chart(pie_playlists)
        col4.plotly_chart(bar_artists)


