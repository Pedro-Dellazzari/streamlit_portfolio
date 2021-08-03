import streamlit as st 

def app():
    #Colocando as categorias de projetos
    st.subheader("Projetos")

    #Descrição
    st.markdown("Essa é minha página de projetos relacionados a Data Science, Data Analytics e Business Intelligence")
    st.markdown("Contato: Pedrocdellazzari@gmail.com | Site: pedrodellazzari.com.br")

    #Criando as colunas
    col1, col2 = st.beta_columns(2)

    #Criando o expander de Data Science 
    data_science = col1.beta_expander("Data Science")
    data_science.write("""- Monitoramento da bolsa de valores indicadas pela CNN \n\n - Projeto 2""")

    #Criando o expander de Machine Learning
    machine_learning = col1.beta_expander("Machine Learning")
    machine_learning.write("""- Recomendações de filmes \n\n - Reconhecimento de imagem""")

    #Criando expander de Data Anlytics 
    data_analyses = col2.beta_expander("Data Analytics")
    data_analyses.write("- Spotify Analyses \n\n - Projeto 2")

    #Criando o expander de inteligencia artificial
    inteligencia = col2.beta_expander("Inteligência Artificial")
    inteligencia.write("- Projeto 1 \n\n - Projeto 2")