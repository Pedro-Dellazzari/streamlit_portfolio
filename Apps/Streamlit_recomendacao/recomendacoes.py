#Importando biblioteca 
from collections import namedtuple
import pandas as pd 
import streamlit as st
import numpy as np
from streamlit.caching import cache
import matplotlib.pyplot as plt

def app():
    # ------ FUNÇÕES --------------
    @st.cache(suppress_st_warning=True)
    def choices(data):

        data = data.reset_index()

        random_number1 = np.random.randint(data.index.min(), data.index.max())

        random_number2 = random_number1 + 10

        dataframe = data[random_number1:random_number2]

        dataframe = dataframe.reset_index()

        return dataframe

    #Função para a diferença de vetores 
    def diferenca_de_vetor(a,b):
        return np.linalg.norm(a - b)

    #Criando função para adicionar novo usário dentro do banco de notas
    def new_user(dados):

        #Criano o id do novo usário 
        iduser = ratings['userId'].max()+1

        #Criando o novo dataset com as notas novas do usuário 
        notas_do_usuario_novo = pd.DataFrame(dados, columns=['movieId', 'rating'])
        notas_do_usuario_novo['userId'] = iduser

        #Concatenando com todas as notas 
        return pd.concat([ratings, notas_do_usuario_novo])

    #Função para pegar as notas do usuário 
    def notas_do_user(userid):
        notas_do_usuario = ratings.query("userId == {}".format(userid))
        notas_do_usuario = notas_do_usuario[['movieId', 'rating']].set_index('movieId')
        return notas_do_usuario

    #Função para fazer a diferença de dois usuários
    def diference_2_user(userid1,userid2):

        #Pegando as notas individuais de cada usuário
        ratings_1 = notas_do_user(userid1)
        ratings_2 = notas_do_user(userid2)

        #Criando join para dataset único 
        notas_total = ratings_1.join(ratings_2, lsuffix='_user1', rsuffix='_user2').dropna()

        #Criar condição para pegar apenas usuários com mais de 5 filmes assistdos em comum 
        if (len(notas_total) < 5):
            return None

        #Calculando a diferença total de usuário 
        return [userid1, userid2, diferenca_de_vetor(notas_total['rating_user1'], notas_total['rating_user2'])]

    #Função para fazer a diferença rodar com todos os usuários dentro do dataset 
    def diference_com_todos(userid):

        #Criando lista 
        diferencas = []

        #Fazendo loop por usuário
        for usuarios in ratings['userId'].unique():
            diferencas.append(diference_2_user(userid, usuarios))

        #Pegando apenas os usuários sem 'none'
        diferencas = list(filter(None,diferencas))

        #Criando o dataset de diferencas
        diferencas = pd.DataFrame(diferencas, columns=['User1','User2','distancia'])
        diferencas = diferencas.sort_values(by='distancia').set_index('User2')
        diferencas = diferencas.drop(userid)

        #Retornando 
        return diferencas

    #Função para pegar apenas os usuários mais próximos
    def mais_proximos(userid):

        #Fazendo as distâncias com todos os usuários
        distancias = diference_com_todos(userid)
        distancias = distancias.sort_values(by='distancia')

        return distancias.head(10)

    #Função para a recomendação de filmes para o determinado usuário 
    def recomendacoes(userid, n_mais_proximos = 5):
        #Pegando os usuários similares 
        similares = mais_proximos(userid)

        #Pegando o valor dos usuários similares 
        usuarios_similares = similares.index

        #Pegando as notas dos usuários similares
        notas_dos_usuarios_similares = ratings.set_index('userId').loc[usuarios_similares]

        #Criando o groupby para pegar as recomendações 
        recomendacoes = notas_dos_usuarios_similares.groupby('movieId')[['rating']].mean()

        #Criando o groupby para as aparicoes do filme 
        aparicoes = notas_dos_usuarios_similares.groupby('movieId')[['rating']].count()

        #Criar um filtro mínimo para pegar os filmes que não forma visto apenas por uma pessoa (usuario similiar)
        filtro_minimo = n_mais_proximos / 2 
        
        #Juntando tudo 
        recomendacoes = recomendacoes.join(aparicoes, lsuffix="_media_dos_users", rsuffix="_aparicoes_filmes")  
        recomendacoes = recomendacoes.query('rating_aparicoes_filmes >= {:.2f}'.format(filtro_minimo))
        recomendacoes = recomendacoes.sort_values('rating_media_dos_users', ascending=False)
        recomendacoes = recomendacoes.join(movies)

        #Pegando filmes com mais de 50 de popularidade 
        #recomendacoes = recomendacoes.query('Popularity > 50')

        #Retornar o dataset de recomendação 
        return recomendacoes

    #Função para pegar o filme e colocar a descrição
    def filme_recomendacao(filme):

        nota = dataset_movies.loc[dataset_movies['title'] == filme, 'rating_media_dos_users'].iloc[0]
        nota = np.round(nota, 2)

        #Arruamdno o título do filme para ficar de acordo com parametors de pesquisa 
        st.write(filme + " -- " + str(nota))

    #Função para plotar os usuários mais próximos 
    def graph_most_similar_users(userid):

        #Pegando as notas do usuário 
        notas_user_primeiras = notas_do_user(userid)['rating'][:5].sum()
        notas_user_ultimas = notas_do_user(userid)['rating'][0:10].sum()

        notas_user = pd.DataFrame({'notas1': notas_user_primeiras, 'notas2': notas_user_ultimas}, index=[0])

        #Pegar os usuários mais similares 
        distancias = mais_proximos(userid)

        #Lista
        notas_primeiras = []
        notas_ultimas = []

        #Pegar
        for user in distancias.index:
            primeiras_notas = notas_do_user(user)['rating'][:5].sum()
            ultimas_notas = notas_do_user(user)['rating'][0:10].sum()

            notas_primeiras.append(primeiras_notas)
            notas_ultimas.append(ultimas_notas)

        #Dataframe
        notas_total = pd.DataFrame()
        notas_total['Range1'] = notas_primeiras
        notas_total['Range2'] = notas_ultimas

        fig, ax = plt.subplots()

        ax.scatter(notas_total['Range1'], notas_total['Range2'], color='black')
        ax.scatter(x=notas_user_primeiras, y=notas_user_ultimas, color='red')
        ax.plot([notas_user_primeiras,notas_total['Range1'][0]],[notas_user_ultimas,notas_total['Range2'][0]], color='grey', linestyle="dashed")
        ax.plot([notas_user_primeiras,notas_total['Range1'][1]],[notas_user_ultimas,notas_total['Range2'][1]], color='grey', linestyle="dashed")
        ax.plot([notas_user_primeiras,notas_total['Range1'][2]],[notas_user_ultimas,notas_total['Range2'][2]], color='grey', linestyle="dashed")
        ax.plot([notas_user_primeiras,notas_total['Range1'][3]],[notas_user_ultimas,notas_total['Range2'][3]], color='grey', linestyle="dashed")
        ax.set_title("Representação gráfica da sua distância com 3 usuários")
        ax.grid(color='grey', linestyle='-', linewidth=1, alpha=0.3)
        
        st.pyplot(fig)


    # --------- DATA ----------
    #Carregando dados 
    movies = pd.read_csv("C:/Users/pedro/Documents/Science/Portfolio-streamlit/Apps/Streamlit_recomendacao/Data/movies.csv")
    ratings = pd.read_csv("C:/Users/pedro/Documents/Science/Portfolio-streamlit/Apps/Streamlit_recomendacao/Data/ratings.csv")

    #Criando a coluna de popularidade do filme 
    popularity = ratings["movieId"].value_counts()

    #Colocando dentro de filmes 
    movies["Popularity"] = popularity

    #Criando a lista de filmes mais populares 
    most_popular_movies = movies.query("Popularity >= 120")

    # ------- APLICATIVO -------------
    #Configurando o título 
    st.title("Recomendação de filmes")

    #Descrição 
    st.write("Aplicativo prático para testar o uso de algoritmo baseados em KNN")
    st.write("Versão - 'BETA'")
    st.write("Caso o aplicativo apresenta falhas ou tem algum sugestão, ficarei feliz em entrar em contato")

    #Fazendo as expander boxes 
    how_it_work = st.beta_expander("Como funciona?")
    how_it_work.write("""O aplicativo recebe as suas notas com 10 filmes aleatórios retirados dentro do dataset do MovieLens.\n
    Com base nessas notas o aplicativo irá criar um algoritmo KNN para tentar encontrar perfis parecidos com o seu baseado na sua distância entre os mesmos \n
    Em outras palavras, o aplicativo fica responsável de encontrar as pessoas mais 'parecidas' contigo""")

    data_spec = st.beta_expander("Dados utilizados")
    data_spec.write("""Os dados utilizados foram do site 'MovieLens', que é gratuito para qualquer usuário""")

    data_usage = st.beta_expander("Utilização de dados")
    data_usage.write("O aplicativo armazena apenas os dados retirados do site MovieLens, todos os dados obtidos durante a utilização serão descartados ao sair da página")

    creditos = st.beta_expander("Créditos")
    creditos.write("""Esse aplicativo foi criado por Pedro Dellazzari\n
    LinkedIn: Pedro Dellazzari\n
    Contato: pedrocdellazzari@gmail.com""")

    #Criando as duas colunas para mostar os inputs de filmes
    col1, col2 = st.beta_columns(2)

    choices(most_popular_movies)

    #Colocando os filmes
    movie_1 = col1.number_input(choices(most_popular_movies)['title'][0], min_value=0, max_value=5)
    movie_2 = col1.number_input(choices(most_popular_movies)['title'][1], min_value=0, max_value=5)
    movie_3 = col1.number_input(choices(most_popular_movies)['title'][2], min_value=0, max_value=5)
    movie_4 = col1.number_input(choices(most_popular_movies)['title'][3], min_value=0, max_value=5)
    movie_5 = col1.number_input(choices(most_popular_movies)['title'][4], min_value=0, max_value=5)

    movie_6 = col2.number_input(choices(most_popular_movies)['title'][5], min_value=0, max_value=5)
    movie_7 = col2.number_input(choices(most_popular_movies)['title'][6], min_value=0, max_value=5)
    movie_8 = col2.number_input(choices(most_popular_movies)['title'][7], min_value=0, max_value=5)
    movie_9 = col2.number_input(choices(most_popular_movies)['title'][8], min_value=0, max_value=5)
    movie_10 = col2.number_input(choices(most_popular_movies)['title'][9], min_value=0, max_value=5)


    #Criando botão para recomendação final
    button = st.button("Ver filmes recomendados")

    #Quando o botão for abertado 
    if button:
        #Criando a lista com as notas do usuário
        user_input = ([choices(most_popular_movies)['movieId'][0], movie_1], 
                    [choices(most_popular_movies)['movieId'][1], movie_2],
                    [choices(most_popular_movies)['movieId'][2], movie_3],
                    [choices(most_popular_movies)['movieId'][3], movie_4],
                    [choices(most_popular_movies)['movieId'][4], movie_5],
                    [choices(most_popular_movies)['movieId'][5], movie_6],
                    [choices(most_popular_movies)['movieId'][6], movie_7],
                    [choices(most_popular_movies)['movieId'][7], movie_8],
                    [choices(most_popular_movies)['movieId'][8], movie_9],
                    [choices(most_popular_movies)['movieId'][9], movie_10]
                    )


        #Criando o novo usuário 
        ratings = new_user(user_input)
        
        #Criando o dataset de filmes indicados 
        dataset_movies = recomendacoes(611)
        
        #Colocando o título de filmes
        st.subheader("Filmes recomendados baseado na nota média dos usuários parecidos com você")

        #Criando as colunas
        col1, col2 = st.beta_columns(2)

        #Utilizando os containers para colocar os filmes recomendados
        with col1:
            for title in dataset_movies['title'][:5]:
                filme_recomendacao(title)

        with col2:
            for title in dataset_movies['title'][5:10]:
                filme_recomendacao(title)

        #Usando a função do gráfico para ilustração gráfica dos usuários
        graph_most_similar_users(ratings['userId'].max())
