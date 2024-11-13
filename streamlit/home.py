from time import time
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_extras.card import card
from streamlit_extras.metric_cards import style_metric_cards

def display_page():
    # Título
    st.title("Olá, nós somos a GasBusters!")

    st.markdown("""
    <p style="background-color:#ff4b4b;border-radius:10px; padding:5px; display:inline-block;">
    Uma equipe de desenvolvedores capacitados para solucionar o seu problema.
    </p>
    """, unsafe_allow_html=True)

    # Exibe a imagem da logo (ajuste para evitar sobreposição)
    st.image("../streamlit/assets/logoGas-removebg-preview.png", caption="Logo da Equipe")

    # Subtítulo
    st.subheader("Compass")

    # Texto
    st.markdown("""
    &nbsp;&nbsp;&nbsp;&nbsp; A **_Compass_** Gás e Energia SA é uma empresa de grande porte localizada no Brasil, 
    atuando no setor de energia. Com uma posição consolidada no mercado, ela se destaca por sua inovação e compromisso com a 
    sustentabilidade e eficiência energética. A empresa está envolvida em várias áreas dentro do setor energético, incluindo a distribuição de gás natural e a implementação de soluções tecnológicas para otimizar o uso de recursos energéticos.
    """)

    # Exibe o vídeo da empresa
    st.video("../streamlit/assets/Compass.mp4")

    # Subtítulo
    st.subheader("Nossa missão")

    # Texto
    st.markdown("""
    &nbsp;&nbsp;&nbsp;&nbsp; O problema a ser abordado neste projeto está relacionado à necessidade de identificar anomalias 
    associadas a fraudes no consumo de gás natural. As fraudes representam não apenas perdas financeiras significativas, 
    mas também riscos à segurança e à confiabilidade do fornecimento. Este projeto visa desenvolver um modelo preditivo 
    que possa detectar padrões suspeitos e comportamentos atípicos no consumo de gás.
    """)

    st.markdown("""
    &nbsp;&nbsp;&nbsp;&nbsp; Neste sentido, a problemática trazida pela empresa, verifica a necessidade de previnir problemas 
    e monitorar o consumo de cada cliente final e distribuidora. A **_Compass_** e a **_IOLIT_**, em parceria com o **_INTELI_** 
    têm o objetivo de desenvolver um modelo preditivo para que seja possível prever possíveis anomalias e problemas na rede de distribuição.
    """)

    def display_team_photos():
        # Título
        st.header("Conheça a equipe GasBusters!")

        # Lista de nomes e imagens dos integrantes (ajuste o caminho das imagens)
        team_members = [
            {"name": "Giacomo Zema", "image": "../streamlit/assets/Giacomo_Zema_Matizonkas (1).jpg"},
            {"name": "Heitor Cândido", "image": "../streamlit/assets/Heitor.jpeg"},
            {"name": "Ian Simão", "image": "../streamlit/assets/Ian_Pereira_Simão (1).jpg"},
            {"name": "Isabelle Pereira", "image": "../streamlit/assets/Isabelle.jpeg"},
            {"name": "Mariana de Paula", "image": "../streamlit/assets/Mariana_de_Paula.jpg"},
            {"name": "Matheus Fernandes", "image": "../streamlit/assets/Matheus_Fernandes.jpg"},
            {"name": "Rafaela Silva", "image": "../streamlit/assets/Rafaela.jpeg"},
            {"name": "Yasmim Passos", "image": "../streamlit/assets/Yasmim.jpeg"},
        ]

        # Loop para organizar 2 fotos por linha
        for i in range(0, len(team_members), 2):
            cols = st.columns(2)  # Cria 2 colunas

            for idx, col in enumerate(cols):
                if i + idx < len(team_members):
                    member = team_members[i + idx]
                    with col:
                        st.image(member['image'], caption=member['name'])

    display_team_photos()


# # Subtítulo
# st.subheader("Integrantes da Equipe")

# # Primeira linha de colunas (4 colunas)
# col1, col2, col3, col4 = st.columns(4)

# with col1:
#     st.image("../streamlit/assets/Giacomo_Zema_Matizonkas.jpg", caption="Giacomo Zema Matizonkas", use_column_width=True)
# with col2:
#     st.image("../streamlit/assets/Rafaela.jpg", caption="Rafaela Silva", use_column_width=True)  # Verifique o caminho
# with col3:
#     st.image("../streamlit/assets/Ian_Pereira_Simão.jpg", caption="Ian Simão", use_column_width=True)  # Verifique o caminho
# with col4:
#     st.image("../streamlit/assets/Isabelle.jpg", caption="Isabelle Pereira", use_column_width=True)  # Verifique o caminho

# # Segunda linha de colunas (4 colunas)
# col5, col6, col7, col8 = st.columns(4)

# with col5:
#     st.image("../streamlit/assets/Mariana_de_Paula_Barbosa_Souza.jpg", caption="Mariana Souza", use_column_width=True)  # Verifique o caminho
# with col6:
#     st.image("../streamlit/assets/Heitor.jpg", caption="Heitor Cândido", use_column_width=True)  # Verifique o caminho
# with col7:
#     st.image("../streamlit/assets/Outro_Integrante1.jpg", caption="Outro Integrante 1", use_column_width=True)  # Verifique o caminho
# with col8:
#     st.image("../streamlit/assets/Outro_Integrante2.jpg", caption="Outro Integrante 2", use_column_width=True)  # Verifique o caminho





