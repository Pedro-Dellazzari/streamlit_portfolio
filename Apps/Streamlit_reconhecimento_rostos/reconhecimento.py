#Importando as bibliotecas 
import streamlit as st
import matplotlib.pyplot as plt 
import cv2
import numpy as np
import PIL.Image

def app():
    #FUNÇÕES 
    #Função analisar imagem 
    def imagem_faces(imagem):
        global faces
        
        imagem = np.array(PIL.Image.open(imagem))
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

        #Pegando os classifador 
        classificador = cv2.CascadeClassifier("Apps/Streamlit_reconhecimento_rostos/classificadores/haarcascade_frontalface_default.xml")

        #Dectando os números de rostos 
        faces = classificador.detectMultiScale(imagem_gray, 1.5, 3)

        #Criando a imagem com os rostos marcados 
        imagem_with_faces = imagem.copy()
        imagem_with_faces = cv2.cvtColor(imagem_with_faces, cv2.COLOR_BGR2RGB)

        #Criando a variável para colocar no texto embaixo dos retângulos
        len_faces = 0

        #Criando a função para criar retângulos nas faces 
        for (x,y,w,h) in faces:
            rectangle = cv2.rectangle(imagem_with_faces, (x,y), (x+w, y+h), (255,127,0), 4)
            cv2.putText(rectangle, "Face_"+str(len_faces), (x,y-10), cv2.FONT_HERSHEY_SIMPLEX,1,(255,127,0),3)

            #Adicionando os valores na variável 
            len_faces = len_faces + 1
            
        #Mostando a imagem 
        return col2.image(imagem_with_faces)

    def show_faces(imagem):
        face_na_imagem = 0 

        imagem_original = np.array(PIL.Image.open(imagem))

        for (x,y,w,h) in faces:
            face_na_imagem += 1

            #Pegando o roi 
            imagem_roi = imagem_original[y:y+h, x:x+w]

            #Transformando a imagem para BGR 
            
            st.image(imagem_roi)

    #APLICATIVO 
    st.title("Reconhecimento de rostos em fotos")
    st.write("Versão - 0.1")
    st.write("Utilize Machine Learning para reconhecer e exportar todos os rostos dentro da sua foto")

    #Imagem do usuário 
    imagem = st.file_uploader("Coloque sua imagem aqui (Em JPG)", type=['jpg'])

    #Botão analisar
    button = st.button("Analisar foto")

    if button:
        col1, col2 = st.beta_columns(2)

        col1.image(imagem)

        imagem_faces(imagem)

        st.subheader("Faces encontradas")

        show_faces(imagem)

