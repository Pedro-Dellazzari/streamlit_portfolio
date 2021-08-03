#Carregando as bibliotecas 
import pandas as pd 
import streamlit as st 
import yfinance as yf

def app():

    #Criando o dataset das ações 
    data = pd.DataFrame({'Ação yfinance': ["PETR4.SA","RAIL3.SA","VALE", "B3SA3.SA", "BBDC4.SA","IGTA3.SA","MYPK3.SA",'MDIA3.SA'],
                'Nome da Ação': ["Petrobras","Rumo","Vale","B3","Bradesco","Iguatemi","Iochpe-Maxion","M.Dias Branco"],
                'Segmento': ['Petróleo Brasileiro S.A. é uma empresa de capital aberto, cujo acionista majoritário é o Governo do Brasil, sendo, portanto, uma empresa estatal de economia mista',
                'A Rumo Logística é uma companhia ferroviária e de logística brasileira, pertencente ao Grupo Cosan.',"Vale é uma mineradora multinacional brasileira e uma das maiores operadoras de logística do país. É uma das maiores empresas de mineração do mundo e também a maior produtora de minério de ferro, de pelotas e de níquel. A empresa também produz manganês, ferroliga, cobre, bauxita, potássio, caulim, alumina e alumínio",
                'B3 é a bolsa de valores oficial do Brasil, sediada na cidade de São Paulo. Em 2017, era a quinta maior bolsa de mercado de capitais e financeiro do mundo, com patrimônio de 13 bilhões de dólares.',
                'Banco Bradesco S.A. é um banco brasileiro, constituído na forma de sociedade anônima, com sede em Osasco, em São Paulo. Foi fundado em 10 de março de 1943 em Marília, em São Paulo, por Amador Aguiar',
                'O Iguatemi Empresa de Shopping Centers S/A é uma empresa brasileira de planejamento, desenvolvimento e administração de shopping centers',
                'A Iochpe-Maxion é uma companhia global, líder mundial na produção de rodas automotivas e um dos principais produtores de componentes estruturais automotivos nas Américas',
                'M. Dias Branco S.A. Indústria e Comércio de Alimentos é uma companhia de alimentos que fabrica, comercializa e distribui biscoitos, massas, bolos, lanches, farinha de trigo, margarinas e gorduras vegetais em todo o Brasil, com sede na cidade de Eusébio, Ceará']})

    #Função para pular linha
    def pular_linha():
        st.text("")

    #Escrevendo o header da página
    st.write("# Aplicação Simples da Bolsa de Valores")
    st.write("1.0")

    #Escrevendo a descrição 
    st.write("### No início do ano a emissora CNN Brasil fez uma matéria contendo as principais ações da Bolsa de Valores para se investir no ano de 2021\n### Esse aplicativo serve para monitorar essas ações")

    #Criando a caixa de seleção 
    pular_linha()
    pular_linha()
    nome_acao = st.selectbox("Selecione a empresa", data["Nome da Ação"])

    #Pegando o valor da Ação na biblioteca do Yfinance 
    tickersymbol = (data["Ação yfinance"][data["Nome da Ação"] == nome_acao].values[0])

    #Pegando os dados 
    tickerdata = yf.Ticker(tickersymbol)

    #Puxando os dados históricos das ações 
    tickerdf = tickerdata.history(period="1d", start="2019-1-1", end="2021-12-31")

    #Escreveno a descrição da empresa selecionada 
    pular_linha()
    st.write("#### Descrição da empresa")
    st.write(data["Segmento"][data["Nome da Ação"] == nome_acao].values[0])
    pular_linha()

    #Criando os gráficos 
    #Gráfico valor de fechamento 
    st.write("## Fechamento por Data")
    st.area_chart(tickerdf.Close)
    pular_linha()


    #Gráfico de volume vendido 
    st.write("## Volume vendido por Data")
    st.bar_chart(tickerdf.Volume)


