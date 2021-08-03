#Importando as bibliotecas 
import pandas as pd 
import matplotlib.pyplot as plt
import numpy 
import requests
import base64
import json
import plotly.express as px
import streamlit as st 

def app():
    global tracks_added
    global tracks_release_data
    global tracks_name
    global tracks_artists
    global tracks_ms
    #Criando a função para a chave de cadastro 


    #Pegando as credenciais
    client_id = 'f458fe65aad84c498981d32b46d9d84e'
    client_secret = '3bfaa00a54d44bae96e1810d90808363'

    #Criando a lista de credenciais 
    client_creds = f"{client_id}:{client_secret}"

    #Fazendo o encoding 
    client_creds_b64 = base64.b64encode(client_creds.encode())

    #Criando os parâmetros para fazer o post do token de acesso
    token_url = 'https://accounts.spotify.com/api/token'
    method = "POST"
    token_data = {'grant_type': "client_credentials"}
    token_header = {"Authorization" : f"Basic {client_creds_b64.decode()}"}

    #Fazendo o post para pegar o token
    response = requests.post(token_url, data=token_data, headers=token_header)

    #Pegando o json 
    token_response = response.json()

    #Pegando o código de acesso 
    access_token = token_response['access_token']


    #Função para pegar todas as playlist 
    def search_playlists(userid):
        global Playlists_df

        #Criando o endpoint
        playlists_url = "https://api.spotify.com/v1/users/{}/playlists".format(userid)

        #Pegando a url 
        playlists_url_full = requests.get(playlists_url, headers={'Authorization':'Bearer ' + access_token})

        #Pegando a resposta em json 
        playlists = playlists_url_full.json()

        #Pegando o nome de todas as playlists 
        names = []
        i = 0 
        for items in playlists['items']:
            names.append(playlists['items'][i]['name'])
            i = i + 1 

        #Pegando o total de músicas dentro de cada playlist 
        tracks = [] 
        i = 0 
        for items in playlists['items']:
            tracks.append(playlists['items'][i]['tracks']['total'])
            i = i + 1 

        #Pegando o ID 
        ID_playlists = []
        i = 0 
        for items in playlists['items']:
            ID_playlists.append(playlists['items'][i]['id'])
            i = i + 1 
        
        #Criando o DataFrame
        Playlists_df = pd.DataFrame()

        #Colocando as informações dentro do dataframe
        Playlists_df["Nome"] = names
        Playlists_df['Tracks'] = tracks
        Playlists_df['ID'] = ID_playlists

        #Retornando o Dataset
        return Playlists_df

    #Função tracks dentro da playlists 
    def search_tracks_playlists(id):
        global play_name
        global tracks_added
        global tracks_release_data
        global tracks_name
        global tracks_artists
        global tracks_ms

        #Criando a url para pegar as músicas da playlist 
        playlists_tracks_url = "https://api.spotify.com/v1/playlists/{}/tracks".format(id)

        #Pegando a response 
        tracks_get = requests.get(playlists_tracks_url, headers={'Authorization':'Bearer ' + access_token})

        #Pegando o json
        tracks = tracks_get.json()


        #Pegando os nomes das playlist 
        tracks_name = []
        i = 0 
        for items in tracks['items']:
            try:
                tracks_name.append(tracks['items'][i]['track']['name'])
                i = i+1
            except:
                i = i+1

        #Pegando o autor da música 
        tracks_artists = []
        i = 0 
        for items in tracks['items']:
            try:
                tracks_artists.append(tracks['items'][i]['track']['artists'][0]['name'])
                i = i + 1
            except:
                i = i+1 

        #Pegando o id do artista 
        #Pensando se precisa pegar ou não

        #Pegando o nome do álbumn
        tracks_album = []
        i = 0 
        for items in tracks['items']:
            try:
                tracks_album.append(tracks['items'][i]['track']['album']['name'])
                i = i + 1 
            except:
                i = i+1

        #Pegando a duração da música em ms 
        tracks_ms = []
        i = 0 
        for items in tracks['items']:
            try:
                tracks_ms.append(tracks['items'][i]['track']['duration_ms'])
                i = i + 1 
            except:
                i = i+1

        #Pegando a data que a música foi adicionada na playlist
        tracks_added = []
        i = 0 
        for items in tracks['items']:
            try:
                tracks_added.append(tracks['items'][i]['added_at'])
                i = i + 1 
            except:
                i = i+1

        #Pegando o dia que a música foi lançada 
        tracks_release_data = []
        i = 0 
        for items in tracks['items']:
            try:
                tracks_release_data.append(tracks['items'][i]['track']['album']['release_date'])
                i = i + 1
            except:
                tracks_release_data.append("0")
                i = i+1

        #Checando os erros
        if len(tracks_added) - len(tracks_name) != 0:
            elems = len(tracks_added) - len(tracks_name)


        #Pegando o nome das playlists
        play_name = []
        for i in tracks['items']:
            play_name.append(Playlists_df['Nome'][Playlists_df['ID']==id].item())

        

    #Web application
    #Colocando o título e subtítulo
    st.title("Playlists analyses - Spotify")
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
    button = st.sidebar.button("Veja seus dados")

    #Quando o botão fro ativado
    if button:

        #Usando a função
        search_playlists(user_id)

        #Criando o Dataset 
        tracks_inside_playlists = pd.DataFrame()

        #Fazendo a função 
        for id in Playlists_df['ID']:
            search_tracks_playlists(id)

        #Colocando os valors dentro da playlists    
        tracks_inside_playlists['playlist'] = play_name

        try:
            tracks_inside_playlists = tracks_inside_playlists.drop(index=tracks_inside_playlists.index[:int(elems)])
        except:
            pass

        #Colocando os valores dentro 
        #Reorganizado os itens 
        try:
            tracks_added = tracks_added[elems:]
            tracks_release_data = tracks_release_data[elems:]
        except:
            pass

        tracks_inside_playlists['added'] = tracks_added
        tracks_inside_playlists['release'] = tracks_release_data
        tracks_inside_playlists['nome'] = tracks_name
        tracks_inside_playlists['artista'] = tracks_artists
        tracks_inside_playlists['duracao'] = tracks_ms

        #Retirando as strings dentro do campo de data 
        tracks_inside_playlists['added'] = tracks_inside_playlists['added'].str.replace("T"," ")
        tracks_inside_playlists['added'] = tracks_inside_playlists['added'].str.replace("Z"," ")

        #Transofmrando a coluna em data 
        tracks_inside_playlists['added'] = pd.to_datetime(tracks_inside_playlists['added'])

        #Pegando o dia da semana e horário que a música foi selecionada
        tracks_inside_playlists["diadasemana"] = tracks_inside_playlists["added"].dt.dayofweek + 1
        tracks_inside_playlists['hora'] = tracks_inside_playlists['added'].dt.hour
        tracks_inside_playlists['added'] = tracks_inside_playlists['added'].dt.date

        #Título após a procuta dos dados 
        st.markdown("<h1 style='text-align:center'>Veja o resultado</h1>", unsafe_allow_html=True)

        #Criando duas colunas para o gráfico de pizza e de barras
        col1, col2 = st.beta_columns(2)

        #Criando o plot de barra
        bar_playlists = px.bar(Playlists_df.sort_values(by='Tracks', ascending=False).head(6), x='Nome', y='Tracks', text='Tracks', color_discrete_sequence=['#1DB954'], width=600)
        bar_playlists.update_xaxes(showline=True, mirror=True, linecolor='black', linewidth=2, tickangle=25)
        bar_playlists.update_yaxes(showline=True, mirror=True, linecolor='black', linewidth=2)
        bar_playlists.update_layout(title_text='Músicas adicionadas por playlist', title_x=0.5)

        #Criando o plot de pizza
        pie_playlists = px.pie(Playlists_df.head(6), values='Tracks', names='Nome', title="Porcentagem músicas por playlist", width=600)
        pie_playlists.update_layout(title_x=0.5)
        
        #Plotando os gráficos nas colunas
        col1.plotly_chart(pie_playlists, use_column_width=True)

        col2.plotly_chart(bar_playlists, use_column_width=True)

        #Fazendo o groupby por música adicionada por data
        songs_per_date = tracks_inside_playlists.groupby(['added','playlist'])['nome'].count().reset_index().sort_values(by='added')

        #Grouby por dia da semana e horário de música adicionados
        songs_per_week_hour = tracks_inside_playlists.groupby(['diadasemana','hora'])['nome'].count().reset_index()

        #Plotando número de músicas adicionadas por playlisy 
        songs_added_thro_time  = px.line(songs_per_date, x='added', y='nome', color='playlist', title='Músicas adicionadas por data e playlist',width=1200)
        songs_added_thro_time.update_layout(title_x=0.5)

        #Colocando o gráfico na página
        st.plotly_chart(songs_added_thro_time, width=3000)
        st.dataframe(tracks_inside_playlists)
        st.dataframe(songs_per_date)

        #Criando o boxplot da data que a música foi lançada
        # Criando o groupby com as datas
        songs_release_dates = tracks_inside_playlists.groupby(['release'])['nome'].count().reset_index().sort_values(by='release')

        #Criando o plotyl 
        songs_realase_date_graph = px.scatter(songs_release_dates, x='release',y='nome', size='nome',title='Datas de lançamento de músicas adicionadas', width=600)
        songs_realase_date_graph.update_layout(title_x=0.5)
        #Criando as colunas
        col1, col2 = st.beta_columns(2)

        #Criando o gráfico de heatmap de dia da semana e horário 
        week_hour_heat = px.density_heatmap(songs_per_week_hour, x='diadasemana',y='hora', nbinsx=7, nbinsy=10, color_continuous_scale='tealgrn', title='Músicas add por dia da semana e hora', width=600)
        week_hour_heat.update_layout(title_x=0.5)

        #Colocando o gráfico na página
        col1.plotly_chart(week_hour_heat) 
        col2.plotly_chart(songs_realase_date_graph)   

        #Fazendo artistas mais escutados 
        songs_per_artists = tracks_inside_playlists.groupby(['artista'])['nome'].count().reset_index().sort_values(by='nome', ascending=False)

        #Fazendo o gra´fico 
        songs_per_artists_graph = px.pie(songs_per_artists.head(5), values='nome', names='artista', title="Maior artista em todas as playlists", width=600)
        songs_per_artists_graph.update_layout(title_x=0.5)
        songs_per_artists_graph_bar = px.bar(songs_per_artists.head(10), x='artista',y='nome', title="Artistas mais add",color_discrete_sequence=['#1DB954'], width=600) 
        songs_per_artists_graph_bar.update_layout(title_x=0.5)
        #Construindo as colunas
        col3, col4 = st.beta_columns(2)

        #Mostrando 
        col3.plotly_chart(songs_per_artists_graph)
        col4.plotly_chart(songs_per_artists_graph_bar)

    
    



