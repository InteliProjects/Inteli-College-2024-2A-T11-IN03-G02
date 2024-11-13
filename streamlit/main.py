import streamlit as st
import pandas as pd
import streamlit_option_menu
from streamlit_option_menu import option_menu

# Importa os outros arquivos com as funções
import predictConsumption
import anomaliaScreen
import home
import doc

# Wide mode
st.set_page_config(layout="wide")


with st.sidebar:    
    selected = option_menu(
    menu_title = "Gas Busters",
    options = ["Home","Predição de Consumo","Anomalias", "Documentação"],
    icons = ["house","calendar-week","activity","book"],
    menu_icon = "fuel-pump-diesel",
    default_index = 0,
    #orientation = "horizontal",
)
    
if selected == "Predição de Consumo":
    predictConsumption.display()

if selected == "Anomalias":
    anomaliaScreen.display()

if selected == "Home":
    home.display_page()

if selected == "Documentação":
    doc.display_doc_page()
    
